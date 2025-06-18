locals {
  domain = "transcribe.l80.ru"
  image  = "ghcr.io/ast21/transcribe-api"
}

job "transcribe" {
  datacenters = ["de1"]

  meta {
    image_tag        = "${IMAGE_TAG}"
    deploy_timestamp = "${DEPLOY_TIMESTAMP}"
  }

  group "svc" {
    count = 1

    network {
      mode = "bridge"

      port "http" {
        to = 8000
      }
    }

    volume "transcribe_cache" {
      type      = "host"
      source    = "transcribe_cache"
      read_only = false
    }

    service {
      tags = [
        "traefik.enable=true",
        "traefik.http.routers.${NOMAD_JOB_NAME}.rule=Host(`${local.domain}`)",
        "traefik.http.routers.${NOMAD_JOB_NAME}.tls=true",
        "traefik.http.routers.${NOMAD_JOB_NAME}.tls.certresolver=leRes",
      ]

      port = "http"

      check {
        type     = "tcp"
        interval = "10s"
        port     = "http"
        path     = "/"
        timeout  = "5s"
      }
    }

    task "server" {
      vault {
        policies = ["access-secrets"]
      }

      driver = "docker"

      config {
        image = "${local.image}:${IMAGE_TAG}"
        auth {
          username = "${GITHUB_USER}"
          password = "${GITHUB_TOKEN}"
        }

        ports = ["http"]
      }

      volume_mount {
        volume      = "transcribe_cache"
        destination = "/root/.cache"
        read_only   = false
      }

      template {
        data        = <<EOF
GITHUB_USER="{{ with secret "secret/data/auth" }}{{ .Data.data.GITHUB_USER }}{{ end }}"
GITHUB_TOKEN="{{ with secret "secret/data/auth" }}{{ .Data.data.GITHUB_TOKEN }}{{ end }}"
EOF
        destination = "secrets/env"
        env         = true
      }

      resources {
        cpu    = 2000
        memory = 2048
      }
    }
  }
}
