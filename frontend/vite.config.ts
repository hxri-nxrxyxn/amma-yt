import tailwindcss from '@tailwindcss/vite';
import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	server: {
		port: 5173,
		proxy: {
			'/api': 'http://127.0.0.1:8000'
		}
	},
	plugins: [
		tailwindcss(),
		sveltekit({
			compilerOptions: {
				runes: ({ filename }) => filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},
			adapter: adapter({
				pages: '../static',
				assets: '../static',
				fallback: 'index.html',
				precompress: false,
				strict: false
			})
		})
	]
});
