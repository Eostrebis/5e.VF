---
title: Classes
---
# Classes de Personnage

<div class="class-grid" id="scoped-content">

	<style type="text/css" scoped>
	/* Grille de classes */
.class-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.class-card {
    background: var(--md-default-bg-color--elevated);
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 8px;
    padding: 0;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    text-decoration: none !important; /* Enlève le souligné du lien */
    color: inherit !important;
    display: flex;
    flex-direction: column;
}

.class-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    border-color: var(--md-accent-fg-color);
}

.class-header {
    background-color: #2e303e; /* Couleur sombre style D&D */
    color: #fff;
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.class-icon {
    font-size: 1.5rem;
}

.class-title {
    font-weight: bold;
    font-size: 1.2rem;
    margin: 0;
}

.class-body {
    padding: 1rem;
    flex-grow: 1;
}

.class-stats {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 1rem;
    background: rgba(0,0,0,0.05);
    font-size: 0.85rem;
    font-weight: bold;
    border-top: 1px solid rgba(0,0,0,0.1);
}

.stat-tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    background-color: var(--md-accent-fg-color--transparent);
    color: var(--md-accent-fg-color);
}
</style>
  <a href="barbare/" class="class-card">
    <div class="class-header">
      <span class="class-icon">🪓</span> <h3 class="class-title">Barbare</h3>
    </div>
    <div class="class-body">
      <p>Un guerrier féroce d'origine primitive qui peut entrer dans une rage de bataille pour résister aux coups.</p>
    </div>
    <div class="class-stats">
      <span>DV: d12</span>
      <span class="stat-tag">Force</span>
    </div>
  </a>

  <a href="barde/" class="class-card">
    <div class="class-header">
      <span class="class-icon">🎵</span>
      <h3 class="class-title">Barde</h3>
    </div>
    <div class="class-body">
      <p>Un magicien inspirant dont le pouvoir résonne dans la musique de la création.</p>
    </div>
    <div class="class-stats">
      <span>DV: d8</span>
      <span class="stat-tag">Charisme</span>
    </div>
  </a>
  
  </div>