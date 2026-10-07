<?php
/**
 * Exposes the deployed build so each deploy can be verified:
 * GET /wp-json/strivesync/v1/build (admins only).
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'rest_api_init',
	function () {
		register_rest_route(
			'strivesync/v1',
			'/build',
			array(
				'methods'             => 'GET',
				'permission_callback' => function () {
					return current_user_can( 'manage_options' );
				},
				'callback'            => function () {
					$build = array( 'commit' => null, 'deployed_at' => null );
					$file  = STRIVESYNC_CORE_DIR . 'BUILD';
					if ( is_readable( $file ) ) {
						$lines                = array_map( 'trim', file( $file ) );
						$build['commit']      = $lines[0] ?? null;
						$build['deployed_at'] = $lines[1] ?? null;
					}
					return array(
						'plugin_version' => STRIVESYNC_CORE_VERSION,
						'commit'         => $build['commit'],
						'deployed_at'    => $build['deployed_at'],
						'theme'          => get_stylesheet(),
						'wp_version'     => get_bloginfo( 'version' ),
						'php_version'    => PHP_VERSION,
					);
				},
			)
		);
	}
);
