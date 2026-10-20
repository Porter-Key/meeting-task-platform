#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SYSTEMD_DIR="${ROOT_DIR}/deploy/systemd"

install -d /var/lib/taskmanagement
install -m 0644 "${SYSTEMD_DIR}/taskmanagement-http.service" /etc/systemd/system/taskmanagement-http.service
install -m 0644 "${SYSTEMD_DIR}/taskmanagement-celery.service" /etc/systemd/system/taskmanagement-celery.service
install -m 0644 "${SYSTEMD_DIR}/taskmanagement-celery-beat.service" /etc/systemd/system/taskmanagement-celery-beat.service

systemctl daemon-reload
systemctl enable taskmanagement-http.service taskmanagement-celery.service taskmanagement-celery-beat.service
systemctl restart taskmanagement-http.service taskmanagement-celery.service taskmanagement-celery-beat.service
systemctl --no-pager --full status taskmanagement-http.service taskmanagement-celery.service taskmanagement-celery-beat.service
