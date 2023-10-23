<script lang="ts">
	import steps from '$lib/data/steps.json';
	import { t, locale, locales } from '$lib/i18n/i18n';
	import predictionImg from '$lib/prediction.png';
	import sehasuLogo from '$lib/images/sehasu-logo.png';
	import Card, { Content, PrimaryAction, Media, MediaContent } from '@smui/card';
	import DataTable, { Head, Body, Row, Cell as DataCell, SortValue } from '@smui/data-table';
	import LayoutGrid, { Cell } from '@smui/layout-grid';
	import IconButton from '@smui/icon-button';
	import Button, { Label, Icon } from '@smui/button';
	import Banner, { Label as BannerLabel } from '@smui/banner';
	import Dialog, { Content as DialogContent } from '@smui/dialog';
	import getUserLocale from 'get-user-locale';

	let userLocale = getUserLocale();
	$locale = userLocale.startsWith('ja') ? 'ja' : userLocale.startsWith('ko') ? 'ko' : 'en';

	let open = false;

	const stepSuccessDetails = [`${$t('step.scDetailPrefix')}03:50${$t('step.scDetailSuffix')}`];
	const stepEndDetails = ['#17'];

	let sortMode = 0; // 0: desc, 1: asc, 2: view desc, 3: view asc

	async function getStats() {
		try {
			const res = await fetch(import.meta.env.VITE_API_URL, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (!res.ok) {
				throw new Error('Error! ' + res.status);
			}

			const result = await res.json();
			return result;
		} catch (error) {
			if (error instanceof Error) {
				console.log('Error message: ', error.message);
				return error.message;
			} else {
				console.log('Unexpected error: ', error);
				return 'An unexpected error occurred.';
			}
		}
	}

	let data = getStats();

	function numberComma(x: number) {
		return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	}

	function getDateString(date: number) {
		const d = new Date(date);
		const year = d.getFullYear();
		const month = d.getMonth() + 1;
		const day = d.getDate();
		const hours = d.getHours();
		const minutes = d.getMinutes();
		return `${year}-${('00' + month.toString()).slice(-2)}-${('00' + day.toString()).slice(-2)} ${(
			'00' + hours.toString()
		).slice(-2)}:${('00' + minutes.toString()).slice(-2)}:00`;
	}

	function sortData(data: any, mode: number) {
		if (mode === 0) {
			return data.slice().reverse();
		} else if (mode === 1) {
			return data;
		} else if (mode === 2) {
			return data.slice().sort((a: any, b: any) => (a.viewCount < b.viewCount ? 1 : -1));
		} else {
			return data.slice().sort((a: any, b: any) => (a.viewCount < b.viewCount ? -1 : 1));
		}
	}
</script>

<svelte:head>
	<title>{$t('title')}</title>
	<meta name="description" content="Sehasu counter" />
</svelte:head>

<section>
	

	<Dialog
		bind:open
		sheet
		aria-describedby="sheet-content"
		surface$style="width: 900px; max-width: calc(100vw - 32px);"
	>
		<DialogContent id="sheet-content">
			<IconButton action="close" class="material-symbols-outlined">close</IconButton>
			<img src={predictionImg} alt="counter" width="100%" />
		</DialogContent>
	</Dialog>

	<LayoutGrid>
		{#await data}
			<Cell
				span={12}
				style="display: flex; justify-content: center; align-items: center; margin-top: 70%; margin-bottom: 30%;"
			>
				<img class="loadingImage" src={sehasuLogo} alt="Loading..." width="150vw" />
			</Cell>
		{:then res}
			<Cell
				span={12}
				style="display: flex; justify-content: center; align-items: center; margin-top: 2rem; margin-bottom: 2rem;"
			>
				<h1>
					{#if $locale === 'en'}
						By {getDateString(res.body.DBtime * 1000)}{@html $t('counter.pre')}<strong
							>{numberComma(res.body.viewSum)}</strong
						>{@html $t('counter.suf')}
					{:else}
						{getDateString(res.body.DBtime * 1000)}{@html $t('counter.pre')}<strong
							>{numberComma(res.body.viewSum)}</strong
						>{@html $t('counter.suf')}
					{/if}
				</h1>
			</Cell>
			<Cell span={12}>
				<DataTable table$aria-label="Steps List" style="width: 100%;">
					<Head>
						<Row>
							<DataCell>{$t('step.number')}</DataCell>
							<DataCell style="width: 100%;">{$t('step.name')}</DataCell>
							<DataCell>{$t('step.start')}</DataCell>
							<DataCell>{@html $t('step.success')}</DataCell>
							<DataCell>{$t('step.end')}</DataCell>
						</Row>
					</Head>
					<Body>
						{#each steps as step (step.number)}
							<Row>
								<DataCell>{step.number}</DataCell>
								<DataCell
									>{#if $locale === 'ja'}
										{@html step.name['ja']}
									{:else if $locale === 'ko' || $locale === 'en'}
										{@html step.name[$locale]}<br /><small>{@html step.name['ja']}</small>
									{/if}</DataCell
								>
								<DataCell>{step.start}</DataCell>
								<DataCell
									><span title={stepSuccessDetails[step.number - 2]}>{@html step.success}</span
									></DataCell
								>
								<DataCell
									><span class="underline" title={stepEndDetails[step.number - 1]}>{step.end}</span
									></DataCell
								>
							</Row>
						{/each}
					</Body>
				</DataTable>
				<div class="predict">
					<Button on:click={() => (open = true)}
						><Icon class="material-symbols-outlined">info</Icon><Label>{$t('detail')}</Label
						></Button
					>
				</div>
				<div>
					<Button on:click={() => (sortMode = (sortMode + 1) % 4)}
						><Icon class="material-symbols-outlined">sort</Icon><Label
							>{$t(`sortMode.${sortMode}`)}</Label
						></Button
					>
				</div>
			</Cell>
			{#each sortData(res.body.videos, sortMode) as video}
				<Cell spanDevices={{ desktop: 3, tablet: 4, phone: 4 }}>
					<div class="card-display">
						<div class="card-container">
							<Card>
								<PrimaryAction
									on:click={() =>
										window.open('https://www.youtube.com/watch?v=' + video.id, '_blank')}
								>
									<Media
										class="card-media-16x9"
										aspectRatio="16x9"
										style="background-image: url(https://i.ytimg.com/vi/{video.id}/sddefault.jpg)"
									>
										<MediaContent>
											<div class="video-upload-date">
												<span class="material-symbols-outlined">calendar_today</span
												>{video.publishedAt}
											</div>
										</MediaContent>
									</Media>
									<Content class="mdc-typography--body2">
										<strong
											>{video.title['ja']}
											{#if $locale === 'ko' || $locale === 'en'}
												<br /><small>{video.title[$locale]}</small>
											{/if}
										</strong><br /><br />
										<div class="video-infos">
											<span class="material-symbols-outlined">visibility</span>{numberComma(
												video.viewCount
											)} views<br /><span class="material-symbols-outlined">favorite</span
											>{numberComma(video.likeCount)} likes<br /><span
												class="material-symbols-outlined">comment</span
											>{numberComma(video.commentCount)} comments
										</div>
									</Content>
								</PrimaryAction>
							</Card>
						</div>
					</div>
				</Cell>
			{/each}
		{/await}
	</LayoutGrid>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

	.material-symbols-outlined {
		vertical-align: middle;
		margin-right: 0.5rem;
		font-variation-settings: 'FILL' 0, 'wght' 600, 'GRAD' 0, 'opsz' 48;
	}

	.video-infos {
		line-height: 1rem;
	}

	.video-upload-date {
		color: #fff;
		position: absolute;
		bottom: 16px;
		right: 16px;
		background-color: #0c0c0c6f;
		text-align: center;
		padding: 0.3rem;
		border-radius: 0.5rem;
	}

	* :global(.mdc-layout-grid__cell--span-3) {
		justify-self: center;
		align-self: center;
	}

	.predict {
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column;
	}

	.loadingImage {
		animation: scaling 1s ease-in-out infinite;
	}

	@keyframes scaling {
		0% {
			transform: scale(1);
			transform-origin: center center;
		}
		50% {
			transform: scale(1.2);
			transform-origin: center center;
		}
		100% {
			transform: scale(1);
			transform-origin: center center;
		}
	}
	.underline {
		border-bottom: 1px dotted black;
	}
</style>
