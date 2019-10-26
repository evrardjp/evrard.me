workflow "Hugo Link Check" {
  resolves = "linkcheck"
  on = "pull_request"
}

action "linkcheck" {
  uses = "marccampbell/hugo-linkcheck-action@v0.1.3"
  env = {
    HUGO_FINAL_URL = "https://evrard.me"
    HUGO_CONFIG = "./config.yaml"
  }
}
