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
        "traefik.http.routers.transcribe.rule=Host(`transcribe.l80.ru`)",
        "traefik.http.routers.transcribe.tls=true",
        "traefik.http.routers.transcribe.tls.certresolver=leRes",
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
        image = "ghcr.io/ast21/transcribe:main"
        auth {
          username = "ast21"
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
