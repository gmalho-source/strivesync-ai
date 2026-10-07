# CLAUDE.md

WordPress site strivesync.ai (theme Salient 18.x + WPBakery, Weglot, Yoast, Fluent Forms, PixelYourSite, Site Kit).

## Rules
- Code goes in `wp-content/plugins/strivesync-core/` (logic) or `wp-content/themes/strivesync-child/` (presentation only). Never touch other plugins or the parent theme.
- New features: one file per feature in `strivesync-core/includes/modules/`, prefix `strivesync_` for functions/hooks, `strivesync/v1` for REST routes.
- Deploy happens only via GitHub Actions on merge to `main`. No direct server edits.
- Content changes go through the REST API (`WP_URL`, `WP_USER`, `WP_APP_PASSWORD`). Create as draft unless told to publish. Page bodies are WPBakery shortcodes: edit `content.raw` (context=edit), never the rendered HTML.
- Weglot translates from the English source; write content in English.
- Run `python3 scripts/wp_snapshot.py` before and after content changes and commit `content/` for history.
- `php -l` every PHP file before pushing.
