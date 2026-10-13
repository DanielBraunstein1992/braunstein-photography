// Formular-Versand über Resend (Vercel Serverless Function, POST /api/anfrage)
// Umgebungsvariablen in Vercel: RESEND_API_KEY, RESEND_FROM, RESEND_TO
const INTERN = new Set(['subject', 'from_name', 'botcheck', 'redirect', 'access_key']);

function maskieren(s) {
  return String(s).replace(/[&<>"']/g, (z) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[z]);
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ success: false });
  }
  const daten = typeof req.body === 'object' && req.body ? req.body : {};
  const alsJson = (req.headers['content-type'] || '').includes('application/json');
  const fertig = (ok, status = 200) => {
    if (alsJson) return res.status(status).json({ success: ok });
    let ziel = '/danke';
    try { if (ok && daten.redirect) ziel = new URL(daten.redirect, 'https://x').pathname; } catch (_) {}
    return ok ? res.redirect(303, ziel) : res.status(status).send('Das hat leider nicht geklappt. Bitte ruft direkt an: +49 176 14362401');
  };

  // Honeypot: Bots füllen das unsichtbare Feld aus, wir tun so, als wäre alles gut
  if (daten.botcheck) return fertig(true);

  const email = String(daten.email || '').trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 200) return fertig(false, 400);

  const felder = Object.entries(daten).filter(([k, v]) => !INTERN.has(k) && String(v).trim() !== '');
  if (felder.length > 30) return fertig(false, 400);
  const zeilen = felder.map(([k, v]) =>
    `<tr><td style="padding:6px 14px 6px 0;vertical-align:top;color:#666;white-space:nowrap">${maskieren(k)}</td>` +
    `<td style="padding:6px 0;white-space:pre-wrap">${maskieren(String(v).slice(0, 5000))}</td></tr>`).join('');
  const betreff = String(daten.subject || 'Neue Anfrage über die Website').slice(0, 150);

  try {
    const antwort = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.RESEND_FROM,
        to: process.env.RESEND_TO.split(',').map((a) => a.trim()),
        reply_to: email,
        subject: betreff,
        html: `<div style="font-family:Arial,sans-serif;font-size:15px;color:#222"><h2 style="font-weight:normal">${maskieren(betreff)}</h2><table>${zeilen}</table></div>`,
        text: felder.map(([k, v]) => `${k}: ${v}`).join('\n'),
      }),
    });
    if (!antwort.ok) {
      console.error('Resend', antwort.status, await antwort.text());
      return fertig(false, 502);
    }
    return fertig(true);
  } catch (fehler) {
    console.error('Resend', fehler);
    return fertig(false, 502);
  }
};
