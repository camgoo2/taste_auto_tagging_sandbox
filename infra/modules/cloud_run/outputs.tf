output "mock_llm_server_url" {
  value = google_cloud_run_service.mock-llm-server.status[0].url
  description = "The url of the deployed Cloud Run Mock LLM Server"
}
