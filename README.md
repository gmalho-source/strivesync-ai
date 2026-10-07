# strivesync.ai — WordPress

Repositório de gestão do site [strivesync.ai](https://strivesync.ai) (WordPress + tema Salient/WPBakery).

## O que vive aqui

| Caminho | Função | Como chega ao site |
|---|---|---|
| `wp-content/plugins/strivesync-core/` | Funcionalidades à medida (CPTs, shortcodes, integrações, endpoints) | Deploy SSH automático |
| `wp-content/themes/strivesync-child/` | Child theme do Salient (CSS, overrides de templates) | Deploy SSH automático |
| `content/` | Snapshot do conteúdo (páginas, posts, menus, media) em JSON | `scripts/wp_snapshot.py` via REST API |
| `.github/workflows/deploy.yml` | Pipeline de deploy | GitHub Actions |

Conteúdo (páginas, posts, SEO) **não** passa pelo deploy: é gerido pela REST API com Application Password.

## Deploy

- Push para `main` com alterações em `wp-content/**` → backup no servidor + rsync + flush de cache.
- Pull request → dry run (mostra o que mudaria, não escreve nada).
- Manual: Actions → *Deploy to strivesync.ai* → *Run workflow* (dry run por defeito).

O rsync com `--delete` está limitado às duas pastas acima. Nada fora delas é tocado (tema Salient, outros plugins, uploads, `wp-config.php`).

Backups ficam em `~/strivesync-backups/` no servidor (últimos 15). Rollback:

```bash
cd <WP_PATH> && tar -xzf ~/strivesync-backups/<timestamp>.tar.gz
```

Verificar o build em produção (admin autenticado): `GET /wp-json/strivesync/v1/build`.

## Secrets necessários (Settings → Secrets and variables → Actions)

| Secret | Exemplo |
|---|---|
| `SSH_HOST` | `strivesync.ai` |
| `SSH_PORT` | `22` |
| `SSH_USER` | `deploy` |
| `SSH_PRIVATE_KEY` | chave privada ed25519 completa (`-----BEGIN OPENSSH PRIVATE KEY-----` …) |
| `WP_PATH` | `/home/xxx/public_html` |
| `SSH_KNOWN_HOSTS` *(opcional, recomendado)* | output de `ssh-keyscan -p <porta> <host>` |

## Child theme — atenção antes de ativar

O site corre hoje o Salient diretamente, sem child theme. Ao trocar de tema, o WordPress perde as definições guardadas por tema: localizações de menus, widgets e Customizer. As opções do Salient (Redux) mantêm-se. Ativar o `strivesync-child` exige reatribuir os menus logo a seguir e deve fazer-se com um backup completo feito. Até lá, o plugin `strivesync-core` é o veículo principal para alterações.
