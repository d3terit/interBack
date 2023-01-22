#[macro_use] extern crate rocket;


#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[get("/hello/<name>/<age>")]
fn hello(name: String, age: u8) -> String {
    format!("Hello, {} year old named {}!", age, name)
}

#[get("/code")]
fn code() -> &'static str {
    r#"{"code": 200, "message": "ok"}"#
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![index, hello, code])
}