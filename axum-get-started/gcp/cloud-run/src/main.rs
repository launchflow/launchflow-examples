use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let lf_env = std::env::var("LAUNCHFLOW_ENVIRONMENT").expect("LaunchFlow environment not set");
    let port = std::env::var("PORT").unwrap_or("3000".to_string());
    let host = std::env::var("HOST").unwrap_or("0.0.0.0".to_string());
    let address = format!("{host}:{port}");

    let greeting = format!("Hello from {lf_env}!");
    let app = Router::new().route("/", get(|| async { greeting }));

    let listener = tokio::net::TcpListener::bind(address).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
