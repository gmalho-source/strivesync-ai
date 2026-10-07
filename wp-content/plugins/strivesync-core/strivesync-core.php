<?php
/**
 * Plugin Name:       Strivesync Core
 * Description:       Funcionalidades à medida do strivesync.ai (gerido via Git + deploy automático).
 * Version:           0.1.0
 * Author:            Strivesync
 * Requires at least: 6.4
 * Requires PHP:      8.0
 * Text Domain:       strivesync-core
 */

defined( 'ABSPATH' ) || exit;

define( 'STRIVESYNC_CORE_VERSION', '0.1.0' );
define( 'STRIVESYNC_CORE_DIR', plugin_dir_path( __FILE__ ) );
define( 'STRIVESYNC_CORE_URL', plugin_dir_url( __FILE__ ) );

/*
 * Each feature lives in its own file under includes/modules/.
 * Files are loaded alphabetically; prefix with a number to control order.
 * To disable a module without deleting it, rename it to *.php.off.
 */
foreach ( glob( STRIVESYNC_CORE_DIR . 'includes/modules/*.php' ) as $strivesync_module ) {
	if ( 'index.php' !== basename( $strivesync_module ) ) {
		require_once $strivesync_module;
	}
}
unset( $strivesync_module );
