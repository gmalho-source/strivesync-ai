<?php
/**
 * Strivesync child theme.
 *
 * Salient enqueues its own parent styles; this only adds the child stylesheet.
 * Keep business logic in the strivesync-core plugin, not here: this file is
 * for presentation (CSS, template overrides) only.
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'wp_enqueue_scripts',
	function () {
		$version = wp_get_theme()->get( 'Version' );
		wp_enqueue_style( 'strivesync-child-style', get_stylesheet_uri(), array(), $version );
	},
	100
);
