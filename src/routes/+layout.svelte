<script>
	import { t, locale, locales } from '$lib/i18n/i18n';
	import './styles.css';
	import { dev } from '$app/environment';
	import { inject } from '@vercel/analytics';
	import { MetaTags } from 'svelte-meta-tags';

	inject({ mode: dev ? 'development' : 'production' });
</script>

<MetaTags
	title={$t('og.title')}
	description={$t('og.description')}
	openGraph={{
		type: 'website',
		url: 'https://sehasu-counter.vercel.app/',
		title: $t('og.title'),
		description: $t('og.description'),
		images: [
			{
				url: 'https://sehasu-counter.s3.ap-northeast-2.amazonaws.com/sehasu-og-image.png',
				alt: 'Sehasu Logo',
				width: 1100,
				height: 740,
				type: 'image/png'
			}
		]
	}}
/>
<!-- <meta property="og:title" content={$t('og.title')} />
<meta property="og:description" content={$t('og.description')} /> -->
<div class="app">
	<main>
		<slot />
	</main>

	<footer>
		<div>
			{@html $t('footer.ifErr')}
		</div>
		<div>
			{@html $t('footer.info')}
		</div>
		<div>
			{@html $t('footer.disclaimer')}
		</div>
		<div>
			<!--カウンター画像からは配布サイトへリンクが設定されています。また、誤作動、誤表示の原因となりますのでコードの改変、改行は行わないで下さい。
このコメント部分は削除して頂いても結構です。-->
			<a href="https://www.free-counter.jp/"
				><img src="https://www.f-counter.net/j/62/1695898520/" alt="アクセスカウンター" /></a
			>
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
		text-align: center;
		padding: 12px;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
