// app.js - Frontend Logic

function scrollToForm() {
    document.getElementById('input-section').scrollIntoView({ behavior: 'smooth' });
}

// UI Toggles
document.querySelectorAll('.platform-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.platform-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

document.querySelectorAll('.tone-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tone-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    });
});

document.getElementById('restartBtn').addEventListener('click', () => {
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('input-section').classList.remove('hidden');
    scrollToForm();
});

document.getElementById('copyAllBtn').addEventListener('click', () => {
    if (!window.lastData) return;
    const data = window.lastData;
    const recHook = data.hooks.hooks.find(h => h.number === data.hooks.recommended_hook_number);
    const textToCopy = `
🎯 RECOMMENDED TOPIC
${data.validation.recommended_topic}
(${data.validation.recommendation_reason})

🎣 WINNING HOOK
"${recHook ? recHook.text : ''}"

✍️ FULL SCRIPT
${data.script.full_script}
`.trim();
    navigator.clipboard.writeText(textToCopy);
    const originalText = document.getElementById('copyAllBtn').innerHTML;
    document.getElementById('copyAllBtn').innerHTML = 'Copied!';
    setTimeout(() => { document.getElementById('copyAllBtn').innerHTML = originalText; }, 2000);
});

// Main Form Submission
document.getElementById('contentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const niche = document.getElementById('niche').value.trim();
    const audience = document.getElementById('audience').value.trim() || 'General';
    const voiceSample = document.getElementById('voiceSample').value.trim();
    const topicIdea = document.getElementById('topicIdea').value.trim();
    const competitors = document.getElementById('competitors').value.split(',').map(s => s.trim()).filter(s => s);
    
    if (!niche || !voiceSample || !topicIdea) {
        alert("Please fill out Niche, Voice Sample, and Topic Idea.");
        return;
    }

    const platform = document.querySelector('.platform-btn.active').dataset.platform;
    const tone = document.querySelector('.tone-btn.active').dataset.tone;

    const payload = {
        niche: niche,
        topic: topicIdea,
        platform: platform,
        tone: tone,
        voice_sample: voiceSample,
        audience: audience,
        competitors: competitors,
        days: 7
    };

    // UI State
    document.getElementById('input-section').classList.add('hidden');
    document.getElementById('processingSection').classList.remove('hidden');
    document.getElementById('processingSection').scrollIntoView({ behavior: 'smooth' });

    // Reset progress
    for(let i=0; i<4; i++) {
        const row = document.getElementById('agentRow' + i);
        row.className = 'agent-row pending';
        document.getElementById('prog' + i).style.width = '0%';
        document.getElementById('progLabel' + i).innerText = 'Waiting...';
    }

    try {
        await runAgentsSequentially(payload);
    } catch (err) {
        alert("Error running pipeline: " + err.message);
        console.error(err);
        document.getElementById('processingSection').classList.add('hidden');
        document.getElementById('input-section').classList.remove('hidden');
    }
});

async function runAgentsSequentially(payload) {
    const apiBase = 'https://contentflow-backend-a450.onrender.com/api/agent';
    let data = {};

    // Helper for fake progress animation
    const animateProgress = (idx, durationMs, labelStr) => {
        const row = document.getElementById('agentRow' + idx);
        row.className = 'agent-row active';
        const prog = document.getElementById('prog' + idx);
        const lbl = document.getElementById('progLabel' + idx);
        lbl.innerText = labelStr;
        
        let w = 0;
        const interval = setInterval(() => {
            w += 2;
            if (w <= 95) prog.style.width = w + '%';
        }, durationMs / 50);
        return interval;
    };

    const finishProgress = (idx, interval) => {
        clearInterval(interval);
        document.getElementById('prog' + idx).style.width = '100%';
        document.getElementById('progLabel' + idx).innerText = 'Complete';
        document.getElementById('agentRow' + idx).className = 'agent-row done';
    };

    // 1. Scraper
    let t1 = animateProgress(0, 1500, 'Scraping feeds...');
    const res1 = await fetch(`${apiBase}/scraper`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ niche: payload.niche, platform: payload.platform, competitors: payload.competitors })
    });
    data.posts = await res1.json();
    finishProgress(0, t1);

    // 2. Validator
    let t2 = animateProgress(1, 1500, 'Validating trends...');
    const res2 = await fetch(`${apiBase}/validator`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ niche: payload.niche, platform: payload.platform, competitors: payload.competitors })
    });
    data.validation = await res2.json();
    finishProgress(1, t2);

    // 3. Script Writer
    let t3 = animateProgress(2, 2000, 'Writing script...');
    const res3 = await fetch(`${apiBase}/script`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ topic: payload.topic, niche: payload.niche, voice_sample: payload.voice_sample, tone: payload.tone, validated_topic: data.validation.recommended_topic })
    });
    data.script = await res3.json();
    finishProgress(2, t3);

    // 4. Hook Gen
    let t4 = animateProgress(3, 1500, 'Generating hooks...');
    const topViews = data.posts.slice(0, 5).map(p => p.views);
    const res4 = await fetch(`${apiBase}/hooks`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ topic: payload.topic, niche: payload.niche, top_views: topViews })
    });
    data.hooks = await res4.json();
    finishProgress(3, t4);

    setTimeout(() => renderResults(data), 500);
}

function renderResults(data) {
    window.lastData = data;
    document.getElementById('processingSection').classList.add('hidden');
    const rs = document.getElementById('resultsSection');
    rs.classList.remove('hidden');
    rs.scrollIntoView({ behavior: 'smooth' });

    // Recommendation Banner
    document.getElementById('recBanner').innerHTML = `
        <div class="rec-title">🎯 AI Recommended Strategy</div>
        <div class="rec-topic">${data.validation.recommended_topic}</div>
        <div class="rec-reason">${data.validation.recommendation_reason}</div>
    `;

    // Tab 1: Scraper
    const tbody = document.getElementById('trendsBody');
    tbody.innerHTML = '';
    data.posts.forEach((p, i) => {
        if(i >= 15) return;
        tbody.innerHTML += `
            <tr>
                <td>${p.rank}</td>
                <td><strong>${p.hook_text}</strong><br><span style="color:var(--muted);font-size:0.8rem">${p.full_caption.substring(0,40)}...</span></td>
                <td>${p.platform}</td>
                <td>${p.format}</td>
                <td>${(p.views/1000).toFixed(1)}K</td>
                <td>${p.engagement_rate}%</td>
                <td>${(p.likes/1000).toFixed(1)}K</td>
                <td>${p.comments}</td>
                <td>${p.post_date}</td>
                <td>${p.viral ? '<span class="viral-tag">🔥 VIRAL</span>' : ''}</td>
            </tr>
        `;
    });

    // Tab 2: Validator
    const vGrid = document.getElementById('validatorGrid');
    vGrid.innerHTML = '';
    data.validation.clusters.forEach(c => {
        vGrid.innerHTML += `
            <div class="cluster-card">
                <h4>${c.label}</h4>
                <div class="cluster-stats">
                    <div>Posts analyzed: <strong>${c.post_count}</strong></div>
                    <div>Avg Views: <strong>${(c.avg_views/1000).toFixed(1)}K</strong></div>
                    <div>Avg ER: <strong>${c.avg_er}%</strong></div>
                    ${c.repeat_viral ? '<div style="color:var(--success)">🔥 Repeat Viral Signal</div>' : ''}
                </div>
            </div>
        `;
    });

    document.getElementById('insightBox').innerHTML = `
        <div style="background:var(--card); padding:20px; border-radius:12px; margin-top:20px; border:1px solid var(--border);">
            <h4>📊 Validation Insights</h4>
            <div style="font-size:0.9rem; color:var(--muted); margin-top:10px; display:flex; flex-direction:column; gap:8px;">
                <div><strong>Filtered out:</strong> ${data.validation.filtered_out} low-performing posts.</div>
                <div><strong>Top Formats:</strong> ${data.validation.top3_formats.join(', ')}</div>
                <div><strong>Sustained Trends:</strong> ${data.validation.sustained_trends.join(', ') || 'None detected'}</div>
            </div>
        </div>
    `;

    // Tab 3: Script
    document.getElementById('voiceAnalysis').innerHTML = `
        <div style="background:var(--card); padding:20px; border-radius:12px; margin-bottom:20px; border:1px solid var(--border);">
            <h4 style="margin-bottom:12px;">🗣️ Voice Breakdown</h4>
            <div style="font-size:0.9rem; color:var(--muted); display:flex; flex-direction:column; gap:8px;">
                <div><strong>Vocabulary:</strong> ${data.script.voice_analysis.vocabulary_words.join(', ')}</div>
                <div><strong>Pacing:</strong> ${data.script.voice_analysis.avg_sentence_length}</div>
                <div><strong>Language:</strong> ${data.script.voice_analysis.hinglish_ratio}</div>
            </div>
        </div>
    `;

    document.getElementById('scriptCard').innerHTML = `
        <div class="script-meta">
            <div><strong>Tone:</strong> ${data.script.voice_analysis.energy}</div>
            <div><strong>Format:</strong> ${data.script.voice_analysis.structure_pattern}</div>
            <div><strong>Length:</strong> ~${data.script.est_duration_sec}</div>
        </div>
        <div class="script-body">${data.script.full_script}</div>
    `;

    // Tab 4: Hooks
    const recHook = data.hooks.hooks.find(h => h.number === data.hooks.recommended_hook_number);
    if(recHook) {
        document.getElementById('recommendedHook').innerHTML = `
            <div class="hook-item recommended" style="margin-bottom:20px;">
                <div class="hook-num">🏆</div>
                <div class="hook-content">
                    <div style="color:var(--success); font-size:0.8rem; font-weight:bold; margin-bottom:6px;">BEST MATCH FOR YOU</div>
                    <div class="hook-text">"${recHook.text}"</div>
                    <div class="hook-meta" style="margin-top:8px;">
                        <span>Pattern: ${recHook.pattern_name}</span>
                        <span>Confidence: ${recHook.confidence_score}/10</span>
                        <span>Matches: ${recHook.matched_reel_views}</span>
                    </div>
                </div>
            </div>
        `;
    }

    const hList = document.getElementById('hooksList');
    hList.innerHTML = '';
    data.hooks.hooks.forEach(h => {
        const isRec = h.number === data.hooks.recommended_hook_number;
        if(isRec) return; // Skip recommended since it's above
        
        hList.innerHTML += `
            <div class="hook-item">
                <div class="hook-num">${h.number}</div>
                <div class="hook-content">
                    <div class="hook-text">"${h.text}"</div>
                    <div class="hook-meta">
                        <span>Pattern: ${h.pattern_name}</span>
                        <span>Confidence: ${h.confidence_score}/10</span>
                        <span>Matches: ${h.matched_reel_views}</span>
                    </div>
                </div>
            </div>
        `;
    });
}
