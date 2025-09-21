from .enums import Language, Framework, DatabaseType


language_prompts = {
    Language.PYTHON: (
        "You are reviewing Python code. Focus on idiomatic usage, PEP 8 style, and common Pythonic patterns. "
        "Refer to the official Python docs: https://docs.python.org/3/. "
    ),
    Language.JAVASCRIPT: (
        "You are reviewing JavaScript code. Consider ES6+ features, async patterns, and browser/node compatibility. "
        "Reference: https://developer.mozilla.org/en-US/docs/Web/JavaScript. "
    ),
    Language.GO: (
        "You are reviewing Go code. Focus on idiomatic Go, error handling, and concurrency patterns. "
        "Refer to: https://golang.org/doc/."
    ),
    Language.RUST: (
        "You are reviewing Rust code. Pay attention to ownership, lifetimes, and idiomatic Rust patterns. "
        "Reference: https://doc.rust-lang.org/book/. "
    ),
    Language.JAVA: (
        "You are reviewing Java code. Focus on OOP principles, Java conventions, and effective use of libraries. "
        "Reference: https://docs.oracle.com/en/java/."
    ),
    Language.TYPESCRIPT: (
        "You are reviewing TypeScript code. Focus on type safety, interfaces, and modern TypeScript features. "
        "Reference: https://www.typescriptlang.org/docs/."
    ),
    Language.CSHARP: (
        "You are reviewing C# code. Focus on .NET conventions, OOP, and idiomatic C# patterns. "
        "Reference: https://learn.microsoft.com/en-us/dotnet/csharp/."
    ),
    Language.CPP: (
        "You are reviewing C++ code. Focus on memory management, modern C++ features, and best practices. "
        "Reference: https://en.cppreference.com/w/."
    ),
    Language.C: (
        "You are reviewing C code. Focus on memory management, pointer safety, and C conventions. "
        "Reference: https://devdocs.io/c/."
    ),
    Language.PHP: (
        "You are reviewing PHP code. Focus on modern PHP practices, security, and code organization. "
        "Reference: https://www.php.net/docs.php."
    ),
    Language.RUBY: (
        "You are reviewing Ruby code. Focus on idiomatic Ruby, OOP, and Ruby conventions. "
        "Reference: https://www.ruby-lang.org/en/documentation/."
    ),
    Language.SWIFT: (
        "You are reviewing Swift code. Focus on safety, protocol-oriented programming, and Swift best practices. "
        "Reference: https://swift.org/documentation/."
    ),
    Language.KOTLIN: (
        "You are reviewing Kotlin code. Focus on null safety, idiomatic Kotlin, and interoperability with Java. "
        "Reference: https://kotlinlang.org/docs/home.html."
    ),
}

framework_prompts = {
    Framework.DJANGO: (
        "You are reviewing Django (Python) code. Focus on Django best practices, ORM usage, and project structure. "
        "Reference: https://docs.djangoproject.com/en/stable/."
    ),
    Framework.FLASK: (
        "You are reviewing Flask (Python) code. Focus on routing, extensions, and idiomatic Flask patterns. "
        "Reference: https://flask.palletsprojects.com/."
    ),
    Framework.FASTAPI: (
        "You are reviewing FastAPI (Python) code. Focus on async patterns, type hints, and dependency injection. "
        "Reference: https://fastapi.tiangolo.com/."
    ),
    Framework.REACT: (
        "You are reviewing React (JavaScript/TypeScript) code. Focus on component structure, hooks, and state management. "
        "Reference: https://react.dev/."
    ),
    Framework.NEXTJS: (
        "You are reviewing Next.js (JavaScript/TypeScript) code. Focus on SSR, routing, and data fetching patterns. "
        "Reference: https://nextjs.org/docs."
    ),
    Framework.EXPRESS: (
        "You are reviewing Express (Node.js) code. Focus on middleware, routing, and async patterns. "
        "Reference: https://expressjs.com/."
    ),
    Framework.ANGULAR: (
        "You are reviewing Angular (TypeScript) code. Focus on component structure, services, and dependency injection. "
        "Reference: https://angular.io/docs."
    ),
    Framework.VUE: (
        "You are reviewing Vue.js (JavaScript) code. Focus on component structure, reactivity, and idiomatic Vue patterns. "
        "Reference: https://vuejs.org/guide/introduction.html."
    ),
    Framework.LARAVEL: (
        "You are reviewing Laravel (PHP) code. Focus on MVC structure, Eloquent ORM, and Laravel conventions. "
        "Reference: https://laravel.com/docs."
    ),

    Framework.GIN: (
        "You are reviewing Gin (Go) code. Focus on routing, middleware, and idiomatic Go patterns. "
        "Reference: https://gin-gonic.com/docs/."
    ),
}

database_prompts = {
    DatabaseType.POSTGRESQL: (
        "You are reviewing PostgreSQL usage. Focus on SQL best practices, schema design, and query optimization. "
        "Reference: https://www.postgresql.org/docs/"),
    DatabaseType.MYSQL: (
        "You are reviewing MySQL usage. Focus on SQL best practices, schema design, and query optimization. "
        "Reference: https://dev.mysql.com/doc/"),
    DatabaseType.SQLITE: (
        "You are reviewing SQLite usage. Focus on lightweight SQL, file-based storage, and schema design. "
        "Reference: https://www.sqlite.org/docs.html"),
    DatabaseType.MONGODB: (
        "You are reviewing MongoDB usage. Focus on schema design, indexing, and aggregation pipelines. "
        "Reference: https://www.mongodb.com/docs/"),
    DatabaseType.REDIS: (
        "You are reviewing Redis usage. Focus on key-value patterns, data structures, and performance. "
        "Reference: https://redis.io/docs/"),
}

