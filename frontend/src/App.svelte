<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApod } from '$lib/services/api';
  import { 
    apodData, 
    isLoading, 
    error, 
    currentDate,
    canGoPrev,
    canGoNext,
    goToPrevDay,
    goToNextDay,
    goToToday
  } from '$lib/stores/apod';

  // Load APOD data when date changes
  async function loadApod(date: string) {
    $isLoading = true;
    $error = null;
    
    try {
      const data = await fetchApod(date);
      $apodData = data;
    } catch (e) {
      $error = e instanceof Error ? e.message : 'An error occurred';
      $apodData = null;
    } finally {
      $isLoading = false;
    }
  }

  // React to date changes
  $: loadApod($currentDate);

  // Handle keyboard navigation
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'ArrowLeft' && $canGoPrev && !$isLoading) {
      goToPrevDay();
    } else if (event.key === 'ArrowRight' && $canGoNext && !$isLoading) {
      goToNextDay();
    }
  }

  onMount(() => {
    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  });

  // Format date for display
  function formatDisplayDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      weekday: 'long',
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }

  // Download HD image
  async function downloadHD() {
    if (!$apodData?.hdurl) return;
    
    const link = document.createElement('a');
    link.href = $apodData.hdurl;
    link.download = `NASA_APOD_${$apodData.date}_${$apodData.title.replace(/[^a-z0-9]/gi, '_')}.jpg`;
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
</script>

<main class="container">
  <header class="header">
    <h1 class="title">
      <span class="title-icon">✦</span>
      NASA APOD
      <span class="title-icon">✦</span>
    </h1>
    <p class="subtitle">Astronomy Picture of the Day</p>
  </header>

  <nav class="navigation">
    <button 
      class="nav-btn prev" 
      on:click={goToPrevDay}
      disabled={!$canGoPrev || $isLoading}
      title="Previous day (←)"
    >
      <span class="nav-arrow">‹</span>
      <span class="nav-text">Previous</span>
    </button>

    <button 
      class="date-display"
      on:click={goToToday}
      disabled={!$canGoNext}
      title="Go to today"
    >
      {formatDisplayDate($currentDate)}
    </button>

    <button 
      class="nav-btn next" 
      on:click={goToNextDay}
      disabled={!$canGoNext || $isLoading}
      title="Next day (→)"
    >
      <span class="nav-text">Next</span>
      <span class="nav-arrow">›</span>
    </button>
  </nav>

  <div class="content">
    {#if $isLoading}
      <div class="loader">
        <div class="loader-ring"></div>
        <p class="loader-text">Loading cosmic wonders...</p>
      </div>
    {:else if $error}
      <div class="error">
        <div class="error-icon">⚠</div>
        <h2>Houston, we have a problem</h2>
        <p>{$error}</p>
        <button class="btn-retry" on:click={() => loadApod($currentDate)}>
          Try Again
        </button>
      </div>
    {:else if $apodData}
      <article class="apod-card">
        <div class="image-container">
          {#if $apodData.media_type === 'video'}
            <iframe 
              src={$apodData.url}
              title={$apodData.title}
              class="apod-video"
              allowfullscreen
            ></iframe>
          {:else}
            <img 
              src={$apodData.url} 
              alt={$apodData.title}
              class="apod-image"
              loading="lazy"
            />
          {/if}
        </div>

        <div class="apod-info">
          <h2 class="apod-title">{$apodData.title}</h2>
          <p class="apod-explanation">{$apodData.explanation}</p>
          
          {#if $apodData.hdurl && $apodData.media_type === 'image'}
            <button class="btn-download" on:click={downloadHD}>
              <span class="btn-icon">⬇</span>
              Download HD
            </button>
          {/if}
        </div>
      </article>
    {/if}
  </div>

  <footer class="footer">
    <p>
      Data provided by 
      <a href="https://api.nasa.gov/" target="_blank" rel="noopener noreferrer">NASA API</a>
    </p>
  </footer>
</main>

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--space-lg);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .header {
    text-align: center;
    margin-bottom: var(--space-xl);
    animation: fadeInDown 0.8s ease-out;
  }

  @keyframes fadeInDown {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .title {
    font-size: clamp(1.5rem, 5vw, 2.5rem);
    background: var(--gradient-aurora);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: var(--space-xs);
  }

  .title-icon {
    display: inline-block;
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(0.9); }
  }

  .subtitle {
    font-size: 1rem;
    color: var(--color-stellar);
    font-weight: 300;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }

  .navigation {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
    flex-wrap: wrap;
    animation: fadeIn 0.8s ease-out 0.2s backwards;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .nav-btn {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-lg);
    background: var(--color-cosmic);
    border: 1px solid var(--color-stellar);
    border-radius: var(--radius-lg);
    color: var(--color-stardust);
    font-size: 0.9rem;
    font-weight: 500;
  }

  .nav-btn:hover:not(:disabled) {
    background: var(--color-stellar);
    border-color: var(--color-aurora);
    box-shadow: var(--shadow-glow);
  }

  .nav-arrow {
    font-size: 1.4rem;
    line-height: 1;
  }

  .date-display {
    padding: var(--space-sm) var(--space-lg);
    background: transparent;
    border: 2px solid var(--color-aurora);
    border-radius: var(--radius-lg);
    color: var(--color-aurora);
    font-family: var(--font-display);
    font-size: 0.85rem;
    letter-spacing: 0.05em;
  }

  .date-display:hover:not(:disabled) {
    background: var(--color-aurora);
    color: var(--color-void);
  }

  .content {
    flex: 1;
    animation: fadeIn 0.8s ease-out 0.4s backwards;
  }

  /* Loader */
  .loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    gap: var(--space-lg);
  }

  .loader-ring {
    width: 60px;
    height: 60px;
    border: 3px solid var(--color-cosmic);
    border-top-color: var(--color-aurora);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .loader-text {
    color: var(--color-stellar);
    font-style: italic;
  }

  /* Error */
  .error {
    text-align: center;
    padding: var(--space-2xl);
    background: var(--color-nebula);
    border-radius: var(--radius-xl);
    border: 1px solid var(--color-nova);
  }

  .error-icon {
    font-size: 3rem;
    margin-bottom: var(--space-md);
  }

  .error h2 {
    color: var(--color-nova);
    margin-bottom: var(--space-sm);
  }

  .error p {
    color: var(--color-stellar);
    margin-bottom: var(--space-lg);
  }

  .btn-retry {
    padding: var(--space-sm) var(--space-xl);
    background: var(--color-nova);
    border: none;
    border-radius: var(--radius-md);
    color: var(--color-moonlight);
    font-weight: 600;
  }

  .btn-retry:hover {
    background: #ff8585;
    transform: translateY(-2px);
  }

  /* APOD Card */
  .apod-card {
    background: var(--color-nebula);
    border-radius: var(--radius-xl);
    overflow: hidden;
    box-shadow: var(--shadow-card);
    border: 1px solid var(--color-cosmic);
  }

  .image-container {
    position: relative;
    background: var(--color-void);
    min-height: 200px;
    max-height: 45vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  .apod-image {
    width: 100%;
    height: 100%;
    max-height: 45vh;
    display: block;
    object-fit: contain;
    transition: transform 0.3s ease;
  }

  .apod-image:hover {
    transform: scale(1.02);
  }

  .apod-video {
    width: 100%;
    aspect-ratio: 16/9;
    border: none;
  }

  .apod-info {
    padding: var(--space-xl);
  }

  .apod-title {
    font-size: clamp(1.2rem, 3vw, 1.8rem);
    color: var(--color-moonlight);
    margin-bottom: var(--space-md);
    line-height: 1.3;
  }

  .apod-explanation {
    color: var(--color-stardust);
    font-size: 1rem;
    line-height: 1.8;
    margin-bottom: var(--space-lg);
    text-align: justify;
    max-height: 25vh;
    overflow-y: auto;
  }

  .btn-download {
    display: inline-flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-lg);
    background: var(--gradient-solar);
    border: none;
    border-radius: var(--radius-md);
    color: var(--color-void);
    font-weight: 600;
    font-size: 0.9rem;
  }

  .btn-download:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(255, 165, 0, 0.4);
  }

  .btn-icon {
    font-size: 1.1rem;
  }

  /* Footer */
  .footer {
    text-align: center;
    padding: var(--space-xl) 0 var(--space-md);
    color: var(--color-stellar);
    font-size: 0.85rem;
  }

  /* Responsive */
  @media (max-width: 600px) {
    .container {
      padding: var(--space-md);
    }

    .nav-text {
      display: none;
    }

    .nav-btn {
      padding: var(--space-sm) var(--space-md);
    }

    .date-display {
      font-size: 0.75rem;
      padding: var(--space-sm) var(--space-md);
    }

    .apod-info {
      padding: var(--space-lg);
    }
  }
</style>
