<script>
	import { t, locale, locales } from '$lib/i18n/i18n';
	import './styles.css';
	import Button, { Label, Icon } from '@smui/button';
	import Banner, { Label as BannerLabel } from '@smui/banner';
	import { dev } from '$app/environment';
	import { inject } from '@vercel/analytics';
	import { MetaTags } from 'svelte-meta-tags';
	// import getUserLocale from 'get-user-locale';

	// let userLocale = getUserLocale();
	// $locale = userLocale.startsWith('ja') ? 'ja' : userLocale.startsWith('ko') ? 'ko' : 'en';

	inject({ mode: dev ? 'development' : 'production' });
</script>

<MetaTags
	title="Se-hasu View Counter"
	description="Se-no de! Hasu no sora! View Counter"
	openGraph={{
		type: 'website',
		url: 'https://sehasu-counter.vercel.app/',
		title: 'Se-hasu View Counter',
		description: 'Se-no de! Hasu no sora! View Counter',
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
	<Banner open centered mobileStacked content$style="max-width: max-content;">
		<BannerLabel slot="label">
			{$t('banner.content')}
			<!-- {$t('banner.content.expectation')} -->
		</BannerLabel>
		<Button slot="actions">{$t('banner.button')}</Button>
	</Banner>
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
