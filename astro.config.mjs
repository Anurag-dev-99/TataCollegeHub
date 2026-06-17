// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://anurag-dev-99.github.io',
  base: '/TataCollegeHub',
  integrations: [sitemap()],
});
