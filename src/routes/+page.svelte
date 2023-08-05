<script lang="ts">
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import Card, {
		Content,
		PrimaryAction,
		Media,
		MediaContent,
		Actions,
		ActionButtons,
		ActionIcons
	} from '@smui/card';
	import LayoutGrid, { Cell } from '@smui/layout-grid';

	// type Video = {
	// 	title: string;
	// 	episode: number;
	// 	id: string;
	// 	viewCount: string;
	// 	likeCount: string;
	// 	commentCount: string;
	// };

	// type Stats = {
	// 	DBtime: string;
	// 	viewSum: number;
	// 	likeSum: number;
	// 	commentSum: number;
	// 	videos: Array<Video>;
	// };

	// type GetCounts = {
	// 	body: Stats;
	// };

	// var count = 0;

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
			//console.log(JSON.stringify(result, null, 4));
			//count = result.body.viewSum;
			//console.log(count);
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

	// let data: any = getStats();
	// async function getPosts() {
	// 	// 원격지 데이터를 fetch로 가져오기
	// 	const res = await fetch(
	// 		'https://2afv7fmrj9.execute-api.ap-northeast-2.amazonaws.com/sehasu/getsehasustats?mode=current'
	// 	);
	// 	const json = await res.json(); // fetch 결과를 JSON 객체로 변환
	// 	count = json.body.viewSum;
	// 	return json; // JSON 객체 반환
	// }
	// let promisePosts = getPosts();
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<LayoutGrid>
		{#await data}
			Loading...
		{:then res}
			<Cell
				span={12}
				style="display: flex; justify-content: center; align-items: center; margin-top: 2rem; margin-bottom: 2rem;"
			>
				<h1>
					By {new Date(res.body.DBtime * 1000)},<br />Se-node Hasunosora! has accumulated
					<strong>{numberComma(res.body.viewSum)}</strong> views.
				</h1>
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
										{video.title}<br /><br />{numberComma(video.viewCount)} views / {numberComma(
											video.likeCount
										)} likes<br />{numberComma(video.commentCount)}
										comments
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

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
