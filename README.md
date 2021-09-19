# <p align="center">Eyes</p>

eyes is a **Public Opinion Mining System** focusing on taiwanese forums such as [PTT](https://www.ptt.cc/bbs/hotboards.html), [Dcard](https://www.dcard.tw/f).

## Features

- :fire: **Article monitor** helps you capture the trend at a glance.

## Screenshots

![Latest Posts](./doc/static/images/articles_dashboard.png)

## Architecture

eyes system architecture

![Architecture](./doc/static/images/architecture.png)

## Tech Stack

### Infrastructure

- Argo Workflow
- Celery, Flower
- Kubernetes, Helm Charts
- MySQL
- Redis

### API

- FastAPI
- SQLAlchemy ORM
- GraphQL

### Web

- React + Redux-Saga
- Tailwind CSS

### ML

- spaCy

## License

[MIT](./LICENSE)
