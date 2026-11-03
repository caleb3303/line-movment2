<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Line Movement Tracker | DraftKings • Full CBB</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background: #0f172a; }
    .alert-pulse { animation: pulse 2s infinite; }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.6; }
    }
  </style>
</head>
<body class="text-slate-100 min-h-screen">

  <header class="bg-slate-900 border-b border-slate-700 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-4">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold">Line Movement Tracker</h1>
          <p class="text-sm text-slate-400">DraftKings • Full College Basketball Slate • Auto-check every 5 min</p>
        </div>
        <div class="flex items-center gap-3 flex-wrap text-sm">
          <div class="bg-slate-800 px-3 py-1.5 rounded-lg">
            Last check: <span id="lastCheck" class="font-mono text-emerald-400">--</span>
          </div>
          <div class="bg-slate-800 px-3 py-1.5 rounded-lg">
            Next check in: <span id="countdown" class="font-mono text-amber-400">5:00</span>
          </div>
          <button onclick="forceCheck()" class="bg-emerald-600 hover:bg-emerald-500 px-4 py-1.5 rounded-lg font-medium">
            Check Now
          </button>
        </div>
      </div>

      <div class="mt-4 flex flex-wrap gap-3 items-center">
        <input id="search" type="text" placeholder="Search teams..." class="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm w-48" />
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" id="alertsOnly" class="rounded" />
          <span class="text-sm">Alerts Only</span>
        </label>
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" id="hasLinesOnly" class="rounded" checked />
          <span class="text-sm">Has Lines Only</span>
        </label>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6">
    <section class="mb-8">
      <h2 class="text-lg font-semibold mb-3 flex items-center gap-2">
        <span class="w-2 h-2 bg-red-500 rounded-full alert-pulse"></span>
        Active Significant Moves
      </h2>
      <div id="alertsContainer" class="space-y-3"></div>
    </section>

    <section>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold">College Basketball Games <span id="gameCount" class="text-slate-400 text-base font-normal"></span></h2>
        <p class="text-xs text-slate-500">Slate date: Nov 3, 2026 (auto-updates daily in full version)</p>
      </div>
      <div id="gamesContainer" class="grid gap-3"></div>
    </section>
  </main>

  <script>
    // Expanded CBB slate (major + secondary games)
    let games = [
      { id:1, away:"Wofford", home:"Tennessee", time:"6:00 PM", open:{spread:-24.5,total:154.5,mlHome:-3500,mlAway:1400}, current:{spread:-25.5,total:156.5,mlHome:-2800,mlAway:1200}, props:[{player:"Chaz Lanier",market:"Points",open:17.5,current:19.5}] },
      { id:2, away:"Manhattan", home:"Kentucky", time:"7:00 PM", open:{spread:-31.5,total:156.5,mlHome:-5000,mlAway:1800}, current:{spread:-33.5,total:158.5,mlHome:-4500,mlAway:1600}, props:[{player:"Otega Oweh",market:"Points",open:15.5,current:18.5}] },
      { id:3, away:"Hampton", home:"Georgia Tech", time:"7:00 PM", open:{spread:-15.5,total:147.5,mlHome:-1100,mlAway:700}, current:{spread:-14.5,total:149.5,mlHome:-950,mlAway:650}, props:[] },
      { id:4, away:"Stetson", home:"South Carolina", time:"7:00 PM", open:{spread:-18.5,total:147.5,mlHome:-1600,mlAway:900}, current:{spread:-19.5,total:149.5,mlHome:-1400,mlAway:850}, props:[] },
      { id:5, away:"Purdue Fort Wayne", home:"Duquesne", time:"7:00 PM", open:{spread:-9.5,total:151.5,mlHome:-450,mlAway:350}, current:{spread:-10.5,total:153.5,mlHome:-480,mlAway:370}, props:[] },
      { id:6, away:"Coppin State", home:"Virginia Tech", time:"7:00 PM", open:{spread:-29.5,total:149.5,mlHome:-4000,mlAway:1500}, current:{spread:-31.5,total:150.5,mlHome:-3800,mlAway:1400}, props:[] },
      { id:7, away:"Holy Cross", home:"Rhode Island", time:"7:00 PM", open:{spread:-18.5,total:146.5,mlHome:-1400,mlAway:850}, current:{spread:-20.5,total:147.5,mlHome:-1600,mlAway:900}, props:[] },
      { id:8, away:"Wagner", home:"Boston College", time:"7:00 PM", open:{spread:-18.5,total:141.5,mlHome:-1400,mlAway:850}, current:{spread:-19.5,total:142.5,mlHome:-1500,mlAway:900}, props:[] },
      { id:9, away:"Drexel", home:"Virginia", time:"7:30 PM", open:{spread:-29.5,total:140.5,mlHome:-4000,mlAway:1500}, current:{spread:-31.5,total:141.5,mlHome:-3800,mlAway:1400}, props:[] },
      { id:10, away:"Sam Houston", home:"Alabama", time:"7:30 PM", open:{spread:-25.5,total:168.5,mlHome:-2800,mlAway:1200}, current:{spread:-26.5,total:171.5,mlHome:-2600,mlAway:1100}, props:[{player:"Mark Sears",market:"Points",open:18.5,current:20.5}] },
      { id:11, away:"New Orleans", home:"LSU", time:"8:00 PM", open:{spread:-24.5,total:156.5,mlHome:-2500,mlAway:1100}, current:{spread:-27.5,total:159.5,mlHome:-2800,mlAway:1200}, props:[] },
      { id:12, away:"Lipscomb", home:"Iowa", time:"8:00 PM", open:{spread:-21.5,total:147.5,mlHome:-1800,mlAway:1000}, current:{spread:-23.5,total:149.5,mlHome:-2000,mlAway:1100}, props:[] },
      { id:13, away:"Alabama State", home:"Texas A&M", time:"8:00 PM", open:{spread:-28.5,total:158.5,mlHome:-3500,mlAway:1400}, current:{spread:-32.5,total:160.5,mlHome:-4000,mlAway:1500}, props:[] },
      { id:14, away:"Cleveland State", home:"Missouri", time:"8:00 PM", open:{spread:-24.5,total:157.5,mlHome:-2500,mlAway:1100}, current:{spread:-26.5,total:159.5,mlHome:-2800,mlAway:1200}, props:[] },
      { id:15, away:"UAPB", home:"Arkansas", time:"8:00 PM", open:{spread:-36.5,total:164.5,mlHome:-6000,mlAway:2000}, current:{spread:-41.5,total:167.5,mlHome:-7000,mlAway:2200}, props:[] },
      { id:16, away:"South Dakota State", home:"Kansas State", time:"8:00 PM", open:{spread:-10.5,total:157.5,mlHome:-500,mlAway:380}, current:{spread:-11.5,total:159.5,mlHome:-550,mlAway:400}, props:[] },
      { id:17, away:"Milligan", home:"UNC Greensboro", time:"7:00 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] },
      { id:18, away:"Warren Wilson", home:"North Carolina A&T", time:"7:00 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] },
      { id:19, away:"Lincoln (MO)", home:"Missouri State", time:"8:00 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] },
      { id:20, away:"Cornell College", home:"Northern Iowa", time:"8:00 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] },
      { id:21, away:"Louisiana Christian", home:"Houston Christian", time:"8:00 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] },
      { id:22, away:"Western New Mexico", home:"New Mexico State", time:"8:30 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] },
      { id:23, away:"Regis", home:"Wyoming", time:"8:30 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] },
      { id:24, away:"Northern Arizona", home:"UNLV", time:"10:00 PM", open:{spread:-20.5,total:151.5,mlHome:-1800,mlAway:1000}, current:{spread:-21.5,total:152.5,mlHome:-1900,mlAway:1050}, props:[] },
      { id:25, away:"Cal State Fullerton", home:"San Diego State", time:"10:00 PM", open:{spread:-15.5,total:152.5,mlHome:-1100,mlAway:700}, current:{spread:-16.5,total:154.5,mlHome:-1200,mlAway:750}, props:[] },
      { id:26, away:"North Florida", home:"California Baptist", time:"10:00 PM", open:{spread:-7.5,total:154.5,mlHome:-320,mlAway:260}, current:{spread:-8.5,total:155.5,mlHome:-350,mlAway:280}, props:[] },
      { id:27, away:"Lewis & Clark", home:"Portland State", time:"10:00 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] },
      { id:28, away:"Bethesda", home:"Pacific", time:"10:00 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] },
      { id:29, away:"Chapman", home:"UC Irvine", time:"10:00 PM", open:{spread:null,total:null,mlHome:null,mlAway:null}, current:{spread:null,total:null,mlHome:null,mlAway:null}, props:[] }
    ];

    let secondsUntilCheck = 300;

    function hasLines(g) {
      return g.current.spread !== null || g.current.total !== null;
    }

    function getTotalMove(g) {
      if (g.open.total === null || g.current.total === null) return 0;
      return Math.abs(g.current.total - g.open.total);
    }

    function isHeavyFavoriteFlip(g) {
      if (g.open.mlHome === null) return { flipped: false };
      const openHomeFav = g.open.mlHome <= -200 || (g.open.spread !== null && g.open.spread <= -7);
      if (openHomeFav && g.current.mlHome > 0) return { flipped: true, team: g.home };
      return { flipped: false };
    }

    function getSignificantProps(g) {
      return (g.props || []).filter(p => Math.abs(p.current - p.open) >= 5);
    }

    function getAlerts(g) {
      const alerts = [];
      const totalMove = getTotalMove(g);
      if (totalMove >= 5) {
        alerts.push({ type: "TOTAL", message: `Total moved ${totalMove.toFixed(1)} pts (${g.open.total} → ${g.current.total})`, severity: totalMove >= 8 ? "high" : "medium" });
      }
      const flip = isHeavyFavoriteFlip(g);
      if (flip.flipped) {
        alerts.push({ type: "FAVORITE_FLIP", message: `${flip.team} opened heavy favorite → now underdog`, severity: "high" });
      }
      getSignificantProps(g).forEach(p => {
        const move = (p.current - p.open).toFixed(1);
        alerts.push({ type: "PROP", message: `${p.player} ${p.market}: ${p.open} → ${p.current} (${move > 0 ? "+" : ""}${move})`, severity: Math.abs(p.current - p.open) >= 8 ? "high" : "medium" });
      });
      return alerts;
    }

    function simulateLineChanges() {
      games.forEach(g => {
        if (!hasLines(g)) return;
        if (Math.random() > 0.4) {
          const delta = (Math.random() * 4 + 0.5) * (Math.random() > 0.5 ? 1 : -1);
          g.current.total = Math.round((g.current.total + delta) * 2) / 2;
        }
        if (Math.random() > 0.7 && g.props.length) {
          const p = g.props[Math.floor(Math.random() * g.props.length)];
          const delta = (Math.random() * 3 + 1) * (Math.random() > 0.5 ? 1 : -1);
          p.current = Math.round((p.current + delta) * 2) / 2;
        }
      });
    }

    function render() {
      const search = document.getElementById("search").value.toLowerCase();
      const alertsOnly = document.getElementById("alertsOnly").checked;
      const hasLinesOnly = document.getElementById("hasLinesOnly").checked;

      let filtered = games.filter(g => {
        if (hasLinesOnly && !hasLines(g)) return false;
        if (search && !(g.away.toLowerCase().includes(search) || g.home.toLowerCase().includes(search))) return false;
        return true;
      });

      if (alertsOnly) filtered = filtered.filter(g => getAlerts(g).length > 0);

      // Alerts
      const allAlerts = [];
      filtered.forEach(g => getAlerts(g).forEach(a => allAlerts.push({...a, game: g})));

      document.getElementById("alertsContainer").innerHTML = allAlerts.length === 0
        ? `<div class="text-slate-500 text-sm py-3">No significant moves detected yet.</div>`
        : allAlerts.map(a => `
          <div class="bg-slate-800 border-l-4 ${a.severity==='high'?'border-red-500':'border-amber-500'} rounded-r-lg p-3 flex justify-between gap-3">
            <div>
              <div class="text-xs text-slate-400 mb-0.5">${a.game.away} @ ${a.game.home}</div>
              <div class="font-medium text-sm">${a.message}</div>
            </div>
            <span class="text-xs px-2 py-0.5 rounded h-fit ${a.severity==='high'?'bg-red-900/50 text-red-300':'bg-amber-900/50 text-amber-300'}">${a.type}</span>
          </div>
        `).join("");

      document.getElementById("gameCount").textContent = `(${filtered.length} shown)`;

      document.getElementById("gamesContainer").innerHTML = filtered.map(g => {
        const alerts = getAlerts(g);
        const totalMove = getTotalMove(g);
        const hasAlert = alerts.length > 0;
        const lined = hasLines(g);

        return `
          <div class="bg-slate-800/70 border ${hasAlert ? 'border-red-500/40' : 'border-slate-700'} rounded-xl p-4">
            <div class="flex justify-between items-start mb-3">
              <div>
                <div class="text-xs text-slate-400 mb-0.5">${g.time} ET</div>
                <h3 class="font-semibold">${g.away} <span class="text-slate-500">@</span> ${g.home}</h3>
              </div>
              ${hasAlert ? '<span class="text-xs bg-red-600 text-white px-2 py-0.5 rounded">MOVE</span>' : ''}
            </div>
            ${lined ? `
              <div class="grid grid-cols-3 gap-2 text-sm">
                <div class="bg-slate-900/40 rounded p-2">
                  <div class="text-xs text-slate-400">Spread</div>
                  <div class="font-mono text-xs">${g.open.spread > 0 ? '+' : ''}${g.open.spread} → <span class="${Math.abs(g.current.spread-g.open.spread)>=2?'text-amber-400 font-bold':''}">${g.current.spread>0?'+':''}${g.current.spread}</span></div>
                </div>
                <div class="bg-slate-900/40 rounded p-2">
                  <div class="text-xs text-slate-400">Total</div>
                  <div class="font-mono text-xs">${g.open.total} → <span class="${totalMove>=5?'text-red-400 font-bold':''}">${g.current.total}</span>${totalMove>=5?` <span class="text-red-400">(+${totalMove.toFixed(1)})</span>`:''}</div>
                </div>
                <div class="bg-slate-900/40 rounded p-2">
                  <div class="text-xs text-slate-400">ML</div>
                  <div class="font-mono text-xs leading-tight">${g.home}: ${g.open.mlHome}→${g.current.mlHome}<br>${g.away}: ${g.open.mlAway>0?'+':''}${g.open.mlAway}→${g.current.mlAway>0?'+':''}${g.current.mlAway}</div>
                </div>
              </div>
            ` : `<div class="text-xs text-slate-500 italic">No betting lines posted yet</div>`}
            ${g.props.length ? `
              <div class="mt-2 pt-2 border-t border-slate-700 text-xs space-y-1">
                ${g.props.map(p => {
                  const m = p.current - p.open;
                  return `<div class="flex justify-between ${Math.abs(m)>=5?'text-amber-300':''}"><span>${p.player} ${p.market}</span><span class="font-mono">${p.open} → ${p.current}${Math.abs(m)>=5?` (${m>0?'+':''}${m.toFixed(1)})`:''}</span></div>`;
                }).join('')}
              </div>
            ` : ''}
          </div>
        `;
      }).join('') || `<div class="text-slate-500 py-8 text-center">No games match filters</div>`;
    }

    function forceCheck() {
      simulateLineChanges();
      document.getElementById("lastCheck").textContent = new Date().toLocaleTimeString();
      secondsUntilCheck = 300;
      render();
    }

    function tick() {
      secondsUntilCheck--;
      if (secondsUntilCheck <= 0) {
        forceCheck();
      }
      const m = Math.floor(secondsUntilCheck / 60);
      const s = secondsUntilCheck % 60;
      document.getElementById("countdown").textContent = `${m}:${s.toString().padStart(2,'0')}`;
    }

    document.getElementById("search").addEventListener("input", render);
    document.getElementById("alertsOnly").addEventListener("change", render);
    document.getElementById("hasLinesOnly").addEventListener("change", render);

    // Initial
    document.getElementById("lastCheck").textContent = new Date().toLocaleTimeString();
    render();
    setInterval(tick, 1000);
  </script>
</body>
</html>