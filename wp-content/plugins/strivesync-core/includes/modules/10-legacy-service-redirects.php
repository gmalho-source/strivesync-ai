<?php
/**
 * 301 redirects for the service pages retired by the AI Systems repositioning
 * (content/proposals/2026-10-ai-systems-repositioning.md).
 *
 * Off by default. Activate, after the pages go to draft, with:
 * POST /wp-json/wp/v2/settings {"strivesync_legacy_redirects_enabled": true}
 *
 * Handles Weglot language prefixes (/ar/services/..., /pt/services/...) by
 * keeping the prefix on the target.
 */

defined( 'ABSPATH' ) || exit;

function strivesync_legacy_redirects_map() {
	return array(
		'services/performance-marketing' => '/services/artificial-intelligence-for-business/',
		'services/brand-strategy'        => '/services/',
	);
}

add_action(
	'init',
	function () {
		register_setting(
			'general',
			'strivesync_legacy_redirects_enabled',
			array(
				'type'         => 'boolean',
				'default'      => false,
				'show_in_rest' => true,
				'description'  => '301 redirects for retired service pages (Performance Marketing, Brand Strategy).',
			)
		);
	}
);

add_action(
	'template_redirect',
	function () {
		if ( ! get_option( 'strivesync_legacy_redirects_enabled', false ) ) {
			return;
		}
		$path = trim( (string) wp_parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ), '/' );
		if ( ! preg_match( '#^((?:[a-z]{2}(?:-[a-z]{2})?/)?)(services/[a-z-]+)$#', $path, $m ) ) {
			return;
		}
		$map = strivesync_legacy_redirects_map();
		if ( ! isset( $map[ $m[2] ] ) ) {
			return;
		}
		$prefix = '' === $m[1] ? '' : '/' . rtrim( $m[1], '/' );
		wp_safe_redirect( home_url( $prefix . $map[ $m[2] ] ), 301, 'Strivesync' );
		exit;
	},
	1
);
