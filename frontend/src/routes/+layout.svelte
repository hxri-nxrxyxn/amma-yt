<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Atom from '@lucide/svelte/icons/atom';

	let { children } = $props();
</script>

<svelte:head>
	<title>Physics with Dhanya</title>
	<link rel="icon" href={favicon} />
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
</svelte:head>

<div class="min-h-screen bg-background text-foreground flex flex-col antialiased w-full max-w-full overflow-x-hidden relative pt-14">
	<!-- Fixed Minimalist Header: Just Physics with Dhanya -->
	<header class="fixed top-0 inset-x-0 z-40 border-b bg-background/95 backdrop-blur px-4 sm:px-6 h-14 flex items-center justify-start w-full">
		<div class="flex items-center gap-2.5">
			<Atom class="size-5" />
			<span class="font-semibold text-base tracking-tight">Physics with Dhanya</span>
		</div>
	</header>

	<div class="flex-1 w-full max-w-full overflow-x-hidden">
		{@render children()}
	</div>
</div>

