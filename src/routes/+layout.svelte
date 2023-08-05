<script>
	import { t, locale, locales } from '$lib/i18n/i18n';
	import './styles.css';
</script>

<div class="app">
	<main>
		<slot />
	</main>

	<footer>
		<div>
			{@html $t('footer.info')}
		</div>
		<div class="issue">
			<a href="https://github.com/AuroraCaelum/TakasakiInfo" style="color: rgb(100, 100, 100);"
				>Report Issue</a
			>
		</div>
		<div>
			{@html $t('footer.disclaimer')}
		</div>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 85rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	footer a {
		font-weight: bold;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
