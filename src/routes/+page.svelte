<script lang="ts">
	import { t, locale, locales } from '$lib/i18n/i18n';
	import Card, { Content, PrimaryAction, Media, MediaContent } from '@smui/card';
	import DataTable, { Head, Body, Row, Cell as DataCell, SortValue } from '@smui/data-table';
	import LayoutGrid, { Cell } from '@smui/layout-grid';
	import getUserLocale from 'get-user-locale';

	var userLocale = getUserLocale();
	$locale = userLocale.startsWith('ja') ? 'ja' : userLocale.startsWith('ko') ? 'ko' : 'en';

	type Steps = {
		number: number;
		start: string;
		success: string;
		end: string;
	};
	let items: Steps[] = [
		{
			number: 1,
			start: '2023-05-02',
			success: '2023-07-07',
			end: '2023-08-04'
		}
	];

	let count = 0;

	async function getStats() {
		try {
			const res = await fetch(
				'https://2afv7fmrj9.execute-api.ap-northeast-2.amazonaws.com/sehasu/getsehasustats?mode=current',
				{
					method: 'GET',
					headers: {
						'Content-Type': 'application/json'
					}
				}
			);

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
</script>

<svelte:head>
	<title>{$t('title')}</title>
	<meta name="description" content="Sehasu counter" />
</svelte:head>

<section>
	<LayoutGrid>
		{#await data}
			<h1>Loading...</h1>
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
				<DataTable table$aria-label="User list" style="width: 100%;">
					<Head>
						<Row>
							<DataCell>{$t('step.number')}</DataCell>
							<DataCell style="width: 100%;">{$t('step.name')}</DataCell>
							<DataCell>{$t('step.start')}</DataCell>
							<DataCell>{$t('step.success')}</DataCell>
							<DataCell>{$t('step.end')}</DataCell>
						</Row>
					</Head>
					<Body>
						{#each items as item (item.number)}
							<Row>
								<DataCell>{item.number}</DataCell>
								<DataCell>{@html $t(`step.${item.number}`)}</DataCell>
								<DataCell>{item.start}</DataCell>
								<DataCell>{item.success}</DataCell>
								<DataCell>{item.end}</DataCell>
							</Row>
						{/each}
					</Body>
				</DataTable>
			</Cell>
			{#each res.body.videos as video}
				<Cell span={3}>
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
										style="background-image: url(https://i.ytimg.com/vi/{video.id}/hq720.jpg)"
									>
										<MediaContent>
											<div style="color: #000; position: absolute; bottom: 16px; left: 16px;" />
										</MediaContent>
									</Media>
									<Content class="mdc-typography--body2">
										{video.title}<br /><br />
										<div class="video-infos">
											<span class="material-symbols-outlined">calendar_today</span
											>{video.publishedAt}<br />
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
</style>
