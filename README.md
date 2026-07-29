# GobTools

Plateforme open source d'outils propulsés par LLM — une alternative modulaire et extensible à Goblin Tools, auto-hébergeable.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌───────────┐
│  Next.js    │────▶│  FastAPI     │────▶│ Providers │
│  Frontend   │     │  Backend     │     │ Ollama    │
│             │     │              │     │ OpenAI    │
│  shadcn/ui  │     │  Plugin      │     │ Anthropic │
│  ReactQuery │     │  Engine      │     │ Gemini    │
│  Tailwind   │     │              │     │ Mistral   │
└─────────────┘     │  PostgreSQL  │     │ OpenRouter│
                    │  Redis       │     └───────────┘
                    └──────────────┘
```

## Démarrage rapide

```bash
cp .env.example .env
# Modifier .env avec vos clés API

# Pour lancer les conteneurs
docker compose -f docker/docker-compose.yml up -d
# Pour arreter les conteneurs
docker compose -f docker/docker-compose.yml down
```

- Frontend : http://localhost:3000
- API : http://localhost:8000
- Documentation interactive : http://localhost:8000/docs
- Métriques : http://localhost:8000/metrics

Stack de monitoring (optionnel) :
```bash
docker compose -f docker/docker-compose.monitoring.yml up -d
```
- Grafana : http://localhost:3001
- Prometheus : http://localhost:9090
- Loki : http://localhost:3100

## Ajouter un outil

Créez un nouveau dossier dans `plugins/` :

```
plugins/mon-outil/
├── manifest.yaml    # Métadonnées
├── prompt.md        # Prompt système
└── icon.svg         # Icône (optionnel)
```

Exemple de `manifest.yaml` :
```yaml
name: Mon Outil
description: Ce qu'il fait
icon: sparkles
temperature: 0.2
category: productivity
```

Le `provider` et le `model` sont définis globalement dans `.env` et s'appliquent à tous les outils.

Aucune modification de code n'est nécessaire — le chargeur de plugins détecte automatiquement les nouveaux outils au démarrage.

## Points d'API

| Méthode | Chemin | Description |
|---------|--------|-------------|
| GET | `/api/v1/tools` | Liste tous les outils |
| GET | `/api/v1/tools/{slug}` | Détail d'un outil |
| POST | `/api/v1/run` | Exécuter un outil |
| POST | `/api/v1/upload/pdf` | Extraire le texte d'un PDF |
| GET | `/api/v1/history` | Historique (paginé) |
| DELETE | `/api/v1/history/{id}` | Supprimer une entrée |
| GET | `/api/v1/favorites` | Liste des favoris |
| POST | `/api/v1/favorites` | Ajouter un favori |
| DELETE | `/api/v1/favorites/{slug}` | Supprimer un favori |
| POST | `/api/v1/export` | Exporter (markdown/txt/json/pdf) |

## Outils disponibles

- **Magic Todo** — Décompose les tâches en sous-tâches
- **Task Master** — Ordonnancement et priorisation des tâches (utilise le résultat de Magic Todo)
- **Professor** — Explication pédagogique de concepts complexes
- **Formalizer** — Professionalise un texte
- **Judge** — Détection et analyse du ton d'un texte
- **Estimator** — Estimation de temps et ressources
- **Conseiller** — Analyse pour/contre pour la prise de décision
- **Chef** — Suggestions de recettes
- **Script d'appel** — Script prêt à lire pour appels téléphoniques
- **Premier Pas** — Première action minuscule pour démarrer une tâche bloquante
- **Routine** — Routines structurées étape par étape
- **Clarté** — Reformulation en langage clair et littéral
- **Brain Dump** — Organisation des pensées
- **Résumeur** — Résumé de textes
- **Traducteur** — Traduction entre langues
- **Correcteur** — Correction orthographique et grammaticale

## Chaînage d'outils

Certains outils peuvent être enchaînés. Par exemple :

1. **Magic Todo** décompose une tâche en sous-tâches
2. Le bouton **"Ordonnancer avec Task Master"** apparaît après l'exécution
3. **Task Master** reçoit automatiquement le résultat de Magic Todo pour le prioriser

Tous les résultats sont persistés en base de données (PostgreSQL) et accessibles via `GET /api/v1/history`.

## Fournisseurs de modèles

Configuration via `.env` :

| Fournisseur | Variable d'env | Modèle par défaut |
|-------------|---------------|-------------------|
| Ollama | `OLLAMA_BASE_URL` | qwen2.5:1.5b |
| OpenAI | `OPENAI_API_KEY` | gpt-4o |
| Anthropic | `ANTHROPIC_API_KEY` | claude-sonnet-4-20250514 |
| Gemini | `GEMINI_API_KEY` | gemini-2.0-flash |
| Mistral | `MISTRAL_API_KEY` | mistral-large-latest |
| OpenRouter | `OPENROUTER_API_KEY` | openai/gpt-4o |

### Ordre de priorité du modèle

1. **Requête API** (`model` dans le body de `POST /api/v1/run`) — priorité maximale
2. **Variable d'environnement** (`LLM_MODEL` dans `.env`) — priorité moyenne
3. **Manifeste du plugin** (`model` dans `plugins/*/manifest.yaml`) — priorité minimale

Le modèle défini dans `.env` écrase donc celui du manifeste de chaque outil.

## Développement

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest tests/ -v
```

### Frontend

```bash
cd frontend
npm install
npm run dev
npm test
```

## Stack technique

- **Frontend :** Next.js 15, TypeScript, TailwindCSS, shadcn/ui, TanStack Query
- **Backend :** Python 3.13, FastAPI, Pydantic, SQLAlchemy, compatible LangGraph
- **Base de données :** PostgreSQL 16, Redis 7
- **Observabilité :** Prometheus, Grafana, Loki
- **Déploiement :** Docker Compose

## Licence

MIT
