import speech_recognition as sr
from .utils.nlp_utils import NLPProcessor
import json
import os
import random
from datetime import datetime
import numpy as np
from typing import List, Dict

class InterviewSystem:
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.recognizer = sr.Recognizer()
        self.questions_db = self._load_questions()
        print(f"Loaded question database keys: {self.questions_db.keys()}")
        self.interview_history_dir = 'data/interview_history'
        os.makedirs(self.interview_history_dir, exist_ok=True)

    def _load_questions(self):
        """Load comprehensive interview questions from database with new quiz format."""
        # This database has been significantly expanded to include more questions
        # across various roles, levels, and focus areas to support a 20-question quiz.
        return {
            'frontend_developer': {
                'entry': {
                    'technical': [
                        {
                            'question': 'Explain the difference between let, const, and var in JavaScript.',
                            'type': 'technical',
                            'context': 'Focus on variable declaration and scope',
                            'keywords': ['hoisting', 'block scope', 'temporal dead zone', 'reassignment', 'immutability'],
                            'options': [
                                "var is function-scoped, let and const are block-scoped.",
                                "let can be reassigned, const cannot, var is always global.",
                                "const allows re-declaration, let and var do not.",
                                "All three are block-scoped but differ in hoisting."
                            ],
                            'correct_option': "var is function-scoped, let and const are block-scoped.",
                            'explanation': "var is function-scoped, meaning its scope is the nearest function. let and const are block-scoped, meaning their scope is limited to the block (curly braces) in which they are defined. const declarations must be assigned at initialization and cannot be reassigned, though the contents of an object or array declared with const can be modified. let can be reassigned but not re-declared in the same same scope. var is hoisted to the top of its function or global scope, initialized with `undefined`, while let and const are also hoisted but remain in a 'temporal dead zone' until their declaration is processed."
                        },
                        {
                            'question': 'What is the Virtual DOM in React and how does it work?',
                            'type': 'technical',
                            'context': 'Explain the concept and its benefits',
                            'keywords': ['virtual dom', 'reconciliation', 'diffing', 'performance', 'rendering'],
                            'options': [
                                "A direct representation of the browser's DOM, used for faster rendering.",
                                "An in-memory representation of the actual DOM, allowing React to optimize updates by comparing a new virtual tree with the previous one.",
                                "A virtual server that pre-renders React components before sending them to the client.",
                                "A feature that allows direct manipulation of the DOM for improved performance."
                            ],
                            'correct_option': "An in-memory representation of the actual DOM, allowing React to optimize updates by comparing a new virtual tree with the previous one.",
                            'explanation': "The Virtual DOM (VDOM) is a lightweight, in-memory representation of the actual DOM. When the state of a component changes, React creates a new Virtual DOM tree. It then efficiently compares this new tree with the previous one using a 'diffing' algorithm. Only the necessary changes (the 'diff') are then applied to the real DOM, minimizing direct DOM manipulation and significantly improving performance, especially for complex UIs."
                        },
                        {
                            'question': 'Explain CSS Box Model and its components.',
                            'type': 'technical',
                            'context': 'Describe the layout model and its properties',
                            'keywords': ['box model', 'content', 'padding', 'border', 'margin'],
                            'options': [
                                "It defines how elements are rendered as a box, including content, padding, border, and margin.",
                                "It's a way to organize JavaScript functions within a global scope.",
                                "It's a CSS property for aligning items in a flex container.",
                                "It's a model for creating responsive layouts using media queries."
                            ],
                            'correct_option': "It defines how elements are rendered as a box, including content, padding, border, and margin.",
                            'explanation': "The CSS Box Model is a fundamental concept in CSS that describes how elements are rendered on a webpage as rectangular boxes. Each box consists of four main components: Content Box (the actual content of the element), Padding Box (transparent area around the content), Border Box (a line around the padding), and Margin Box (transparent area outside the border, separating it from other elements). Understanding this model is crucial for layout and spacing in web design."
                        },
                        {
                            'question': 'How does event delegation work in JavaScript?',
                            'type': 'technical',
                            'context': 'Explain its advantages and use cases.',
                            'keywords': ['event delegation', 'event bubbling', 'event listener', 'performance'],
                            'options': [
                                "It involves attaching multiple event listeners to each individual element.",
                                "It attaches a single event listener to a parent element, which then listens for events bubbling up from its children.",
                                "It's a technique for preventing events from propagating up the DOM tree.",
                                "It allows events to be triggered in a specific order, regardless of DOM structure."
                            ],
                            'correct_option': "It attaches a single event listener to a parent element, which then listens for events bubbling up from its children.",
                            'explanation': "Event delegation is a technique where you attach a single event listener to a parent element, rather than attaching separate listeners to each child element. When an event (like a click) occurs on a child element, it 'bubbles up' the DOM tree to its parent. The single event listener on the parent then catches the event and can identify which child element originally triggered it. This approach is highly efficient for dynamic lists or large numbers of elements, as it reduces memory consumption and improves performance by minimizing the number of event listeners."
                        },
                        {
                            'question': 'Describe the purpose of Webpack in a frontend project.',
                            'type': 'technical',
                            'context': 'Focus on bundling, asset management, and development features.',
                            'keywords': ['webpack', 'module bundler', 'asset management', 'loaders', 'plugins', 'dev server'],
                            'options': [
                                "A JavaScript framework for building user interfaces.",
                                "A database management system for frontend data.",
                                "A static module bundler for modern JavaScript applications, used to compile modules into a single bundle, manage assets, and provide development utilities.",
                                "A tool for deploying web applications to production servers."
                            ],
                            'correct_option': "A static module bundler for modern JavaScript applications, used to compile modules into a single bundle, manage assets, and provide development utilities.",
                            'explanation': "Webpack is a powerful static module bundler for modern JavaScript applications. Its main purpose is to take various assets (JavaScript, CSS, images, fonts) and transform them into a production-ready bundle. It uses 'loaders' to process different file types and 'plugins' to perform custom operations like optimization, asset management, and environment variable injection. Webpack also offers development features like hot module replacement (HMR) for a faster development workflow."
                        },
                        {
                            'question': 'Explain the concept of immutability in React state management.',
                            'type': 'technical',
                            'context': 'Discuss its benefits and how to achieve it.',
                            'keywords': ['immutability', 'react state', 'pure functions', 'performance', 'mutability'],
                            'options': [
                                "Directly modifying state objects to update the UI efficiently.",
                                "Creating new copies of state objects instead of modifying existing ones, which helps with change detection and avoids side effects.",
                                "Storing all state in a global variable for easy access.",
                                "A pattern used only for functional components, not class components."
                            ],
                            'correct_option': "Creating new copies of state objects instead of modifying existing ones, which helps with change detection and avoids side effects.",
                            'explanation': "Immutability in React means that you do not directly modify state objects or props. Instead, whenever state needs to change, you create a new copy of the state with the desired modifications. This is beneficial for: 1. Predictability: Makes it easier to reason about how data changes. 2. Performance: React's reconciliation process relies on shallow comparisons, and creating new object references helps React detect changes more efficiently. 3. Debugging: Easier to track changes and debug issues. It is achieved using techniques like spread syntax (`...`), `Object.assign()`, or immutable utility libraries (e.g., Immer)."
                        }
                    ],
                    'problem_solving': [
                        {
                            'question': 'How would you optimize a slow-loading webpage?',
                            'type': 'problem_solving',
                            'context': 'Consider both frontend and backend optimizations',
                            'keywords': ['lazy loading', 'caching', 'minification'],
                            'options': [
                                "Increase server response time and use larger image files.",
                                "Minimize HTTP requests, optimize images, enable caching, and use lazy loading for non-critical assets.",
                                "Use synchronous JavaScript loading and avoid content delivery networks.",
                                "Prioritize render-blocking CSS and JavaScript."
                            ],
                            'correct_option': "Minimize HTTP requests, optimize images, enable caching, and use lazy loading for non-critical assets.",
                            'explanation': "Optimizing a slow-loading webpage involves several techniques: minimizing HTTP requests (e.g., by combining files, using CSS sprites), optimizing image sizes and formats, enabling browser and server caching, using lazy loading for images and videos below the fold, minifying CSS and JavaScript files, and using a Content Delivery Network (CDN) for faster asset delivery. Prioritizing critical rendering path assets can also help with perceived performance."
                        },
                         {
                            'question': 'Describe a strategy for handling asynchronous operations in JavaScript.',
                            'type': 'problem_solving',
                            'context': 'Discuss Promises, async/await, and callbacks.',
                            'keywords': ['asynchronous', 'promises', 'async/await', 'callbacks', 'event loop'],
                            'options': [
                                "Perform all operations synchronously to avoid complexity.",
                                "Use Promises for single asynchronous tasks, and async/await for more readable sequential asynchronous code, while understanding callbacks as the foundational pattern.",
                                "Avoid asynchronous operations in web development entirely.",
                                "Rely solely on setTimeout for all asynchronous tasks."
                            ],
                            'correct_option': "Use Promises for single asynchronous tasks, and async/await for more readable sequential asynchronous code, while understanding callbacks as the foundational pattern.",
                            'explanation': "Handling asynchronous operations in JavaScript is crucial for non-blocking UIs. Common strategies include: 1. Callbacks: Functions passed as arguments to be executed later, though they can lead to 'callback hell' for nested operations. 2. Promises: Objects representing the eventual completion or failure of an asynchronous operation, providing a more structured way to handle async code with `.then()` and `.catch()`. 3. Async/Await: Syntactic sugar built on Promises, making asynchronous code look and behave more like synchronous code, significantly improving readability and error handling with `try...catch`."
                        },
                        {
                            'question': 'How would you approach cross-browser compatibility issues?',
                            'type': 'problem_solving',
                            'context': 'Discuss tools and techniques for ensuring consistent behavior.',
                            'keywords': ['cross-browser', 'compatibility', 'polyfills', 'babel', 'autoprefixer', 'normalize.css'],
                            'options': [
                                "Only develop for a single browser (e.g., Chrome).",
                                "Ignore older browsers and focus only on the latest versions.",
                                "Use browser developer tools for testing, employ polyfills for missing features, use transpilers (e.g., Babel), CSS prefixes (e.g., Autoprefixer), and CSS resets/normalizers.",
                                "Write entirely separate codebases for each browser."
                            ],
                            'correct_option': "Use browser developer tools for testing, employ polyfills for missing features, use transpilers (e.g., Babel), CSS prefixes (e.g., Autoprefixer), and CSS resets/normalizers.",
                            'explanation': "Ensuring cross-browser compatibility means making sure your web application works consistently across different web browsers and versions. Strategies include: 1. Testing: Regularly test across target browsers (manual and automated). 2. Polyfills: JavaScript code that provides modern functionality for older browsers. 3. Transpilers (Babel): Convert modern JavaScript (ES6+) to older versions (ES5) compatible with more browsers. 4. CSS Prefixes (Autoprefixer): Automatically add vendor prefixes for CSS properties. 5. CSS Resets/Normalizers: Reset browser-specific default styles to a consistent baseline. 6. Feature Detection: Using JavaScript to check for browser support for a feature before using it."
                        },
                        {
                            'question': 'You are integrating a third-party API that frequently changes. How do you design your frontend to be resilient to these changes?',
                            'type': 'problem_solving',
                            'context': 'Discuss abstraction, versioning, and error handling.',
                            'keywords': ['api integration', 'resilience', 'abstraction', 'versioning', 'error handling', 'middleware'],
                            'options': [
                                "Directly call the API from every component and tightly couple to its structure.",
                                "Avoid using third-party APIs entirely.",
                                "Create an abstraction layer (e.g., a service or adapter) to encapsulate API calls, use API versioning, implement robust error handling with fallbacks, and use automated integration tests.",
                                "Manually update all API calls in every component whenever the API changes."
                            ],
                            'correct_option': "Create an abstraction layer (e.g., a service or adapter) to encapsulate API calls, use API versioning, implement robust error handling with fallbacks, and use automated integration tests.",
                            'explanation': "To make a frontend resilient to frequently changing third-party APIs: 1. Abstraction Layer: Create a dedicated service or adapter module that encapsulates all API interactions. Your components interact only with this layer, not directly with the API. This way, if the API changes, you only modify the adapter. 2. API Versioning: Leverage API versioning (e.g., `/api/v1/data`, `/api/v2/data`) to allow for gradual migration. 3. Robust Error Handling: Implement comprehensive error handling (e.g., try-catch blocks, circuit breakers, retries) with graceful fallbacks. 4. Automated Tests: Write integration tests for the API abstraction layer to catch breaking changes early. 5. Monitoring & Alerting: Monitor API health and set up alerts for errors or performance degradation."
                        }
                    ],
                    'system_design': [
                        {
                            'question': 'Design a simple client-side caching mechanism for a web application.',
                            'type': 'system_design',
                            'context': 'Consider local storage, session storage, and service workers.',
                            'keywords': ['caching', 'local storage', 'session storage', 'service worker', 'performance'],
                            'options': [
                                "Store all data directly in JavaScript variables.",
                                "Use server-side rendering exclusively to avoid client-side caching.",
                                "Employ Local Storage for persistent data, Session Storage for session-specific data, and Service Workers for more advanced caching strategies like offline access and asset caching.",
                                "Disable all caching to ensure the latest data is always fetched."
                            ],
                            'correct_option': "Employ Local Storage for persistent data, Session Storage for session-specific data, and Service Workers for more advanced caching strategies like offline access and asset caching.",
                            'explanation': "A robust client-side caching mechanism can significantly improve web application performance and user experience. Common strategies include: 1. Local Storage: Stores data persistently across browser sessions (e.g., user preferences). 2. Session Storage: Stores data only for the duration of a browser session (e.g., form data). 3. Service Workers: Powerful JavaScript files that run in the background, intercepting network requests and allowing for fine-grained control over caching, enabling features like offline capabilities and faster subsequent loads."
                        },
                         {
                            'question': 'How would you design the data flow for a real-time chat application?',
                            'type': 'system_design',
                            'context': 'Focus on client-server communication and message persistence.',
                            'keywords': ['real-time', 'websockets', 'message queue', 'database', 'scalability'],
                            'options': [
                                "Use traditional HTTP requests for all messages.",
                                "Implement long polling for message updates.",
                                "Utilize WebSockets for persistent, full-duplex communication between clients and server, potentially with a message queue for scalability and a database for message persistence.",
                                "Send messages via email for reliability."
                            ],
                            'correct_option': "Utilize WebSockets for persistent, full-duplex communication between clients and server, potentially with a message queue for scalability and a database for message persistence.",
                            'explanation': "Designing a real-time chat application typically involves: 1. WebSockets: Essential for persistent, bidirectional communication between client and server, enabling instant message delivery. 2. Backend Server: Handles WebSocket connections, message routing, and interacts with storage. 3. Message Queue (e.g., Kafka, RabbitMQ): For scalability, messages can be pushed to a queue for asynchronous processing and delivery to multiple connected clients. 4. Database (e.g., PostgreSQL, MongoDB): For persisting chat messages and user data. Considerations also include user authentication, presence (online/offline status), and handling message delivery guarantees."
                        },
                        {
                            'question': 'Design a responsive navigation bar for a large-scale web application.',
                            'type': 'system_design',
                            'context': 'Consider different breakpoints, accessibility, and performance.',
                            'keywords': ['responsive design', 'navigation bar', 'hamburger menu', 'accessibility', 'performance', 'css media queries'],
                            'options': [
                                "Use a fixed navigation bar that doesn't change on smaller screens.",
                                "Hide the navigation bar completely on mobile devices.",
                                "Implement a flexible layout using CSS Grid or Flexbox, utilize media queries for breakpoints (e.g., hamburger menu on mobile), ensure ARIA attributes for accessibility, and optimize for performance.",
                                "Create separate HTML files for desktop and mobile navigation."
                            ],
                            'correct_option': "Implement a flexible layout using CSS Grid or Flexbox, utilize media queries for breakpoints (e.g., hamburger menu on mobile), ensure ARIA attributes for accessibility, and optimize for performance.",
                            'explanation': "Designing a responsive navigation bar involves adapting its layout and functionality across various screen sizes. Key aspects: 1. Flexible Layouts: Use CSS Grid or Flexbox for dynamic arrangement. 2. Media Queries: Apply different styles at specific breakpoints (e.g., transforming a full menu into a hamburger icon on mobile). 3. Accessibility: Ensure proper ARIA attributes, keyboard navigation, and focus management. 4. Performance: Optimize images, minimize JavaScript, and consider lazy loading for off-screen navigation elements. 5. User Experience: Clear visual cues for interactive elements and intuitive navigation pathways."
                        },
                        {
                            'question': 'How would you design a dark mode feature for an existing web application?',
                            'type': 'system_design',
                            'context': 'Consider CSS variables, user preference, and persistence.',
                            'keywords': ['dark mode', 'theming', 'css variables', 'user preference', 'local storage', 'accessibility'],
                            'options': [
                                "Create an entirely separate CSS file for dark mode and swap it manually.",
                                "Only implement dark mode for a specific browser.",
                                "Utilize CSS variables (custom properties) for colors, allowing easy theme switching; detect user's system preference (`prefers-color-scheme`), and persist their choice using Local Storage.",
                                "Force all users into dark mode without an option to switch."
                            ],
                            'correct_option': "Utilize CSS variables (custom properties) for colors, allowing easy theme switching; detect user's system preference (`prefers-color-scheme`), and persist their choice using Local Storage.",
                            'explanation': "Designing a dark mode feature involves providing an alternative color palette. Key design considerations: 1. CSS Variables: Define color schemes using CSS custom properties (`--primary-color: #xxx;`). Switching themes then means updating these variables. 2. User Preference Detection: Use the `prefers-color-scheme` media query to automatically apply dark mode if the user's operating system is set to it. 3. Persistence: Store the user's explicit dark/light mode choice in Local Storage so it persists across sessions. 4. Accessibility: Ensure sufficient contrast for both themes. 5. Semantic Colors: Use abstract color names (e.g., `--text-color-primary`) instead of literal color names (`--black`) for easier maintenance."
                        }
                    ],
                    'behavioral': [
                        {
                            'question': 'Describe a conflict you had with a teammate or manager and how you resolved it.',
                            'type': 'behavioral',
                            'context': 'Focus on your communication and conflict resolution skills.',
                            'keywords': ['conflict resolution', 'communication', 'teamwork', 'collaboration', 'negotiation'],
                             'options': [
                                "I avoided the conflict entirely and hoped it would resolve itself.",
                                "I confronted the person aggressively to get my way.",
                                "I initiated a private conversation to understand their perspective, expressed my concerns calmly, and worked collaboratively to find a mutually agreeable solution.",
                                "I reported the issue to HR immediately without attempting to resolve it directly."
                            ],
                            'correct_option': "I initiated a private conversation to understand their perspective, expressed my concerns calmly, and worked collaboratively to find a mutually agreeable solution.",
                            'explanation': "Effective conflict resolution involves active listening to understand the other party's viewpoint, clearly articulating your own concerns in a calm and respectful manner, focusing on the problem rather than personal attacks, and collaboratively working towards a solution that benefits all parties. Seeking mediation if direct resolution isn't possible is also a valid step."
                        },
                        {
                            'question': 'How do you stay updated with the latest frontend technologies and trends?',
                            'type': 'behavioral',
                            'context': 'Discuss your learning habits and resources.',
                            'keywords': ['continuous learning', 'tech trends', 'frontend community', 'blogs', 'conferences'],
                            'options': [
                                "I only learn new technologies when required by a specific project.",
                                "I regularly read tech blogs, attend webinars/conferences, participate in online communities, and experiment with new tools in personal projects.",
                                "I rely solely on my teammates to inform me of new developments.",
                                "I believe staying updated is not essential for experienced developers."
                            ],
                            'correct_option': "I regularly read tech blogs, attend webinars/conferences, participate in online communities, and experiment with new tools in personal projects.",
                            'explanation': "Staying updated in the fast-paced frontend world requires continuous learning. This can involve reading industry blogs (e.g., CSS-Tricks, Smashing Magazine), following key figures on social media, attending virtual or in-person conferences and meetups, participating in online forums or communities (e.g., Stack Overflow, Discord channels), contributing to open-source projects, and actively experimenting with new frameworks, libraries, or tools in personal projects."
                        },
                        {
                            'question': 'Describe a time you received constructive criticism and how you responded to it.',
                            'type': 'behavioral',
                            'context': 'Focus on your ability to receive feedback and grow.',
                            'keywords': ['feedback', 'constructive criticism', 'growth mindset', 'learning', 'self-improvement'],
                            'options': [
                                "I became defensive and disregarded the feedback.",
                                "I passively accepted the feedback without making any changes.",
                                "I listened actively, asked clarifying questions, reflected on the feedback, and took actionable steps to incorporate it into my work, demonstrating a commitment to continuous improvement.",
                                "I only accept feedback from people I consider experts."
                            ],
                            'correct_option': "I listened actively, asked clarifying questions, reflected on the feedback, and took actionable steps to incorporate it into my work, demonstrating a commitment to continuous improvement.",
                            'explanation': "Receiving constructive criticism effectively is a sign of professionalism and a growth mindset. A good approach involves: 1. Active Listening: Pay full attention without interrupting. 2. Clarifying Questions: Ask to ensure you fully understand the feedback. 3. Reflection: Take time to process the feedback calmly. 4. Actionable Steps: Identify specific actions you can take to address the feedback. 5. Follow-up: Demonstrate that you've implemented the changes. This process shows a commitment to self-improvement and helps build trust."
                        }
                    ]
                },
                'mid': {
                    'technical': [
                        {
                            'question': 'Explain the concept of closures in JavaScript with examples.',
                            'type': 'technical',
                            'context': 'Focus on practical applications and use cases',
                            'keywords': ['closure', 'scope', 'lexical environment', 'private variables', 'function factory', 'data privacy'],
                            'options': [
                                "A closure is a function that has access to its own scope and the global scope, but not the outer function's scope.",
                                "A closure is the combination of a function bundled together (enclosed) with references to its surrounding state (the lexical environment).",
                                "A closure is a technique to prevent variable hoisting in JavaScript.",
                                "A closure is a type of loop that iterates over an array."
                            ],
                            'correct_option': "A closure is the combination of a function bundled together (enclosed) with references to its surrounding state (the lexical environment).",
                            'explanation': "A closure is a powerful feature in JavaScript where a function 'remembers' the environment (its lexical scope) in which it was created, even after the outer function has finished executing. This means a function can still access variables from its parent scope. Common applications include data privacy (creating private variables), function factories, and maintaining state in event handlers or callbacks."
                        },
                        {
                            'question': 'Discuss the performance considerations when working with large lists in React.',
                            'type': 'technical',
                            'context': 'Mention techniques like virtualization and memoization.',
                            'keywords': ['react performance', 'list rendering', 'virtualization', 'memoization', 'react.memo', 'useCallback', 'useMemo'],
                            'options': [
                                "Render all list items simultaneously, regardless of visibility.",
                                "Use `ReactDOM.render()` repeatedly for each list item update.",
                                "Employ techniques like list virtualization (rendering only visible items) and memoization (`React.memo`, `useCallback`, `useMemo`) to prevent unnecessary re-renders of list items.",
                                "Store all list data in global state to avoid performance issues."
                            ],
                            'correct_option': "Employ techniques like list virtualization (rendering only visible items) and memoization (`React.memo`, `useCallback`, `useMemo`) to prevent unnecessary re-renders of list items.",
                            'explanation': "Rendering large lists in React can lead to performance issues due to the overhead of creating and updating many DOM nodes. Key optimization techniques include: 1. List Virtualization (Windowing): Libraries like `react-window` or `react-virtualized` render only the items currently visible in the viewport, significantly reducing DOM elements. 2. Memoization: Using `React.memo` for functional components, `useCallback` for functions, and `useMemo` for values can prevent unnecessary re-renders of list items when their props or dependencies haven't changed."
                        },
                        {
                            'question': 'Explain the differences between client-side rendering (CSR) and server-side rendering (SSR).',
                            'type': 'technical',
                            'context': 'Discuss their pros and cons for different applications.',
                            'keywords': ['csr', 'ssr', 'hydration', 'seo', 'performance', 'user experience'],
                            'options': [
                                "CSR renders pages on the server, while SSR renders them in the browser.",
                                "CSR delivers an empty HTML shell and JavaScript, rendering content in the browser, while SSR sends a fully rendered HTML page from the server.",
                                "SSR is only used for static websites, and CSR is for dynamic applications.",
                                "There are no significant differences between CSR and SSR."
                            ],
                            'correct_option': "CSR delivers an empty HTML shell and JavaScript, rendering content in the browser, while SSR sends a fully rendered HTML page from the server.",
                            'explanation': "Client-Side Rendering (CSR) involves the browser receiving a minimal HTML file and JavaScript. The browser then fetches data and renders the content dynamically. Pros: Faster initial page load (perceived), good for rich interactive applications. Cons: Slower Time To Interactive (TTI), worse for SEO. Server-Side Rendering (SSR) means the server renders the full HTML page with content and sends it to the browser. Pros: Better SEO, faster initial page load (actual content). Cons: Can be slower Time To First Byte (TTFB) due to server processing, requires server resources. 'Hydration' is the process where CSR takes over an SSR-rendered page to make it interactive."
                        },
                        {
                            'question': 'Explain the concept of Server-Side Rendering (SSR) in React and its benefits.',
                            'type': 'technical',
                            'context': 'Focus on initial load, SEO, and hydration.',
                            'keywords': ['ssr', 'server-side rendering', 'react', 'next.js', 'hydration', 'seo', 'performance'],
                            'options': [
                                "Rendering React components directly in the browser after all JavaScript is loaded.",
                                "Pre-rendering React components on the server into HTML, which is then sent to the client and re-hydrated by React on the browser.",
                                "A technique for building RESTful APIs with React.",
                                "Using React to manage server logic and database interactions."
                            ],
                            'correct_option': "Pre-rendering React components on the server into HTML, which is then sent to the client and re-hydrated by React on the browser.",
                            'explanation': "Server-Side Rendering (SSR) in React involves pre-rendering React components into HTML on the server. This HTML is then sent to the client, providing a faster initial page load and better SEO because search engine crawlers can see fully rendered content immediately. Once the HTML arrives, React 'hydrates' the page by attaching JavaScript event listeners and making the page interactive. Popular frameworks like Next.js simplify SSR in React."
                        },
                        {
                            'question': 'Describe the challenges of state management in large React applications and common solutions.',
                            'type': 'technical',
                            'context': 'Discuss prop drilling, Context API, and external libraries.',
                            'keywords': ['state management', 'react', 'prop drilling', 'context api', 'redux', 'zustand', 'global state'],
                            'options': [
                                "State management is never a challenge in React applications.",
                                "The main challenge is deciding between functional and class components.",
                                "Challenges include prop drilling and ensuring consistent data across components. Solutions involve using React Context API for simpler global state or external libraries like Redux, Zustand, or Recoil for more complex, scalable state management.",
                                "All state should always be lifted to the topmost parent component."
                            ],
                            'correct_option': "Challenges include prop drilling and ensuring consistent data across components. Solutions involve using React Context API for simpler global state or external libraries like Redux, Zustand, or Recoil for more complex, scalable state management.",
                            'explanation': "In large React applications, state management can become complex due to issues like 'prop drilling' (passing props down many levels) and maintaining consistent state across distant components. Solutions include: 1. React Context API: Suitable for less frequently updated global state, avoiding prop drilling for certain data. 2. External Libraries: Redux provides a centralized store with predictable state changes, while more modern, lightweight options like Zustand, Recoil, and Jotai offer simpler APIs for managing global state. The choice depends on application complexity, performance needs, and team preference."
                        }
                    ],
                    'problem_solving': [
                        {
                            'question': 'Describe how you would debug a complex frontend application in a production environment.',
                            'type': 'problem_solving',
                            'context': 'Tools and strategies for production debugging.',
                            'keywords': ['debugging', 'production', 'monitoring', 'logging', 'devtools', 'sentry'],
                            'options': [
                                "Add `console.log` statements directly into production code and deploy.",
                                "Rely solely on local development environment debugging.",
                                "Utilize production monitoring tools (e.g., Sentry, New Relic) for error tracking and performance, leverage browser developer tools for live inspection, and use source maps for readable production code.",
                                "Ask users to send screenshots of errors."
                            ],
                            'correct_option': "Utilize production monitoring tools (e.g., Sentry, New Relic) for error tracking and performance, leverage browser developer tools for live inspection, and use source maps for readable production code.",
                            'explanation': "Debugging complex frontend applications in production requires a systematic approach. Key strategies include: 1. Production Monitoring & Error Tracking: Tools like Sentry, LogRocket, or New Relic collect real-time error reports, performance metrics, and user session replays. 2. Browser Developer Tools: Even in production, these allow inspection of the DOM, network requests, console logs, and performance profiles. 3. Source Maps: Essential for mapping minified/uglified production code back to original source code for easier debugging in the browser. 4. Centralized Logging: Implementing robust client-side logging that sends relevant information to a central logging service can provide context for production issues without impacting user experience directly."
                        },
                        {
                            'question': 'You are tasked with improving the accessibility (A11y) of an existing web application. What steps would you take?',
                            'type': 'problem_solving',
                            'context': 'Discuss WCAG, ARIA, and testing methodologies.',
                            'keywords': ['accessibility', 'a11y', 'wcag', 'aria', 'semantic html', 'keyboard navigation', 'screen reader', 'testing'],
                            'options': [
                                "Assume the application is accessible by default.",
                                "Only focus on visual design, ignoring keyboard navigation.",
                                "Conduct accessibility audits (manual/automated), use semantic HTML, add ARIA attributes where needed, ensure keyboard navigability and sufficient color contrast, and test with screen readers.",
                                "Remove all interactive elements to simplify the UI."
                            ],
                            'correct_option': "Conduct accessibility audits (manual/automated), use semantic HTML, add ARIA attributes where needed, ensure keyboard navigability and sufficient color contrast, and test with screen readers.",
                            'explanation': "Improving web accessibility (A11y) involves making web applications usable by people with disabilities. Key steps: 1. Audits: Perform manual (keyboard navigation, screen reader testing) and automated (Lighthouse, Axe) audits. 2. Semantic HTML: Use appropriate HTML5 elements (e.g., `<button>`, `<nav>`) for their inherent accessibility. 3. ARIA Attributes: Use WAI-ARIA attributes (`aria-label`, `role`, `aria-hidden`) to provide semantic meaning where native HTML isn't sufficient. 4. Keyboard Navigability: Ensure all interactive elements are accessible via keyboard (`Tab`, `Enter`). 5. Color Contrast: Verify sufficient contrast for both themes. 6. Screen Reader Testing: Use tools like VoiceOver (macOS), NVDA (Windows) to experience the site as a screen reader user."
                        }
                    ],
                    'system_design': [
                        {
                            'question': 'How would you architect a scalable user authentication system for a web application?',
                            'type': 'system_design',
                            'context': 'Consider JWT, OAuth, and session management.',
                            'keywords': ['authentication', 'jwt', 'oauth', 'session management', 'scalability', 'security'],
                            'options': [
                                "Store user credentials directly in the client-side code.",
                                "Use basic HTTP authentication for all requests.",
                                "Implement a token-based system (e.g., JWT) for stateless authentication, or a session-based system with a distributed session store for scalability, potentially integrating with OAuth for third-party logins.",
                                "Allow anonymous access to all features to simplify authentication."
                            ],
                            'correct_option': "Implement a token-based system (e.g., JWT) for stateless authentication, or a session-based system with a distributed session store for scalability, potentially integrating with OAuth for third-party logins.",
                            'explanation': "A scalable user authentication system typically involves: 1. Token-Based Authentication (e.g., JWT): Stateless, meaning the server doesn't need to store session information. Tokens are signed and contain user data, allowing for easy scaling across multiple servers. 2. Session-Based Authentication: Requires server-side session management, often stored in a distributed cache (e.g., Redis) for scalability. 3. OAuth: For allowing users to log in with third-party providers (Google, Facebook) without sharing their credentials directly with your application. Security considerations include using HTTPS, proper hashing of passwords, and secure token handling."
                        },
                        {
                            'question': 'Design a component library structure for a large-scale React project.',
                            'type': 'system_design',
                            'context': 'Focus on reusability, consistency, and maintainability.',
                            'keywords': ['component library', 'design system', 'react', 'storybook', 'reusability', 'maintainability'],
                            'options': [
                                "Put all components in a single file.",
                                "Create a new component for every slight variation of an existing component.",
                                "Establish a clear folder structure (e.g., atomic design), define clear component APIs, use tools like Storybook for documentation and testing, and ensure consistent styling guidelines.",
                                "Allow each developer to structure components as they see fit."
                            ],
                            'correct_option': "Establish a clear folder structure (e.g., atomic design), define clear component APIs, use tools like Storybook for documentation and testing, and ensure consistent styling guidelines.",
                            'explanation': "Designing a component library for a large React project ensures reusability, consistency, and maintainability. Key aspects include: 1. Folder Structure: Often follows principles like Atomic Design (Atoms, Molecules, Organisms, Templates, Pages). 2. Clear Component APIs: Define clear props and events for each component to ensure predictable behavior. 3. Documentation & Testing: Tools like Storybook provide an isolated environment for developing, documenting, and testing UI components. 4. Styling Consistency: Enforce a design system with consistent styling (e.g., using CSS-in-JS, CSS Modules, or Sass) and theming capabilities. 5. Versioning and Distribution: How the library is shared and consumed across multiple projects."
                        },
                        {
                            'question': 'Design a client-side routing system for a Single Page Application (SPA).',
                            'type': 'system_design',
                            'context': 'Consider history API, URL structure, and component loading.',
                            'keywords': ['spa', 'client-side routing', 'history api', 'react router', 'vue router', 'lazy loading', 'component loading'],
                            'options': [
                                "Reload the entire page for every navigation.",
                                "Use hash-based routing (#/path) for all routes.",
                                "Utilize the History API (`pushState`, `popState`) to change URLs without full page reloads, define clear route configurations, and dynamically load components as needed (lazy loading).",
                                "Manage routing solely through server-side redirects."
                            ],
                            'correct_option': "Utilize the History API (`pushState`, `popState`) to change URLs without full page reloads, define clear route configurations, and dynamically load components as needed (lazy loading).",
                            'explanation': "Client-side routing in an SPA allows for navigation without full page reloads, providing a smoother user experience. Key aspects: 1. History API: Modern browsers provide `pushState()` and `popState()` to manipulate the browser's history and URL without a server request. 2. URL Structure: Define clear and consistent URL patterns for different views/components. 3. Component Loading: Dynamically load (lazy load) components only when their route is activated, improving initial load performance. Libraries like React Router or Vue Router abstract away much of the complexity, handling URL parsing, component mapping, and history management."
                        }
                    ],
                    'behavioral': [
                        {
                            'question': 'Describe a significant technical challenge you faced as a mid-level frontend developer and how you overcame it.',
                            'type': 'behavioral',
                            'context': 'Focus on your problem-solving process and learning.',
                            'keywords': ['technical challenge', 'problem solving', 'learning', 'resilience', 'resourcefulness'],
                            'options': [
                                "I gave up when faced with a difficult problem.",
                                "I asked a senior developer to solve it for me without trying myself.",
                                "I broke down the problem, researched solutions, experimented with different approaches, sought feedback when stuck, and learned from the experience, ultimately resolving it.",
                                "I ignored the challenge and moved on to easier tasks."
                            ],
                            'correct_option': "I broke down the problem, researched solutions, experimented with different approaches, sought feedback when stuck, and learned from the experience, ultimately resolving it.",
                            'explanation': "When facing technical challenges, a strong problem-solving process involves: 1. Understanding the Problem: Clearly define the issue and its scope. 2. Breaking Down: Divide the problem into smaller, manageable parts. 3. Research: Look for existing solutions, documentation, and similar cases. 4. Experimentation: Try different approaches and test their effectiveness. 5. Seeking Help: Don't hesitate to ask for help from peers or mentors after you've exhausted your own efforts. 6. Learning: Reflect on the process and what you learned to improve for future challenges."
                        },
                        {
                            'question': 'How do you prioritize tasks and manage your time effectively in a fast-paced environment?',
                            'type': 'behavioral',
                            'context': 'Discuss your time management strategies.',
                            'keywords': ['time management', 'prioritization', 'productivity', 'organization', 'agile'],
                            'options': [
                                "I work on whatever task I feel like at the moment.",
                                "I let my manager prioritize all my tasks for me.",
                                "I use techniques like the Eisenhower Matrix (Urgent/Important), set clear deadlines, break down large tasks, and regularly review my progress, adapting as priorities shift.",
                                "I only focus on tasks that are easy to complete quickly."
                            ],
                            'correct_option': "I use techniques like the Eisenhower Matrix (Urgent/Important), set clear deadlines, break down large tasks, and regularly review my progress, adapting as priorities shift.",
                            'explanation': "Effective time management and prioritization in a fast-paced environment are critical. Strategies include: 1. Prioritization Frameworks: Using methods like the Eisenhower Matrix (categorizing tasks as Urgent/Important) or MoSCoW (Must-have, Should-have, Could-have, Won't-have) to determine task order. 2. Breaking Down Tasks: Dividing large tasks into smaller, manageable steps. 3. Setting Realistic Deadlines: Ensuring tasks have clear timelines. 4. Avoiding Multitasking: Focusing on one task at a time for better concentration. 5. Regular Review: Periodically assessing progress and re-prioritizing as needed, especially in agile environments."
                        }
                    ]
                },
                'senior': {
                    'technical': [
                        {
                            'question': 'Discuss advanced state management patterns in React (e.g., Redux, Context API, Zustand).',
                            'type': 'technical',
                            'context': 'Compare their use cases, pros, and cons.',
                            'keywords': ['state management', 'redux', 'context api', 'zustand', 'recoil', 'jotai', 'global state'],
                            'options': [
                                "Only local component state is ever needed for complex applications.",
                                "All state should be managed using the `useState` hook in the top-level component.",
                                "Evaluate solutions like Redux for large, complex applications requiring strict data flow, Context API for simpler global state or prop drilling reduction, and lightweight alternatives like Zustand/Recoil for modern use cases, choosing based on project scale and team familiarity.",
                                "State management is primarily handled by the backend."
                            ],
                            'correct_option': "Evaluate solutions like Redux for large, complex applications requiring strict data flow, Context API for simpler global state or prop drilling reduction, and lightweight alternatives like Zustand/Recoil for modern use cases, choosing based on project scale and team familiarity.",
                            'explanation': "Advanced state management in React is crucial for complex applications. Common patterns include: 1. Redux: A predictable state container for JavaScript apps, known for its strict unidirectional data flow and powerful debugging tools, ideal for large-scale applications. 2. Context API: A built-in React feature for passing data through the component tree without prop drilling, suitable for less frequently updated global state. 3. Modern Alternatives (Zustand, Recoil, Jotai): Lightweight, performant, and often simpler alternatives to Redux, offering a more 'React-ish' feel for global state management with less boilerplate. The choice depends on project size, complexity, and team preferences."
                        },
                        {
                            'question': 'Explain the concept of Web Components and their benefits.',
                            'type': 'technical',
                            'context': 'Discuss Custom Elements, Shadow DOM, and HTML Templates.',
                            'keywords': ['web components', 'custom elements', 'shadow dom', 'html templates', 'reusability', 'interoperability'],
                            'options': [
                                "Web Components are a proprietary Google technology for Chrome browsers.",
                                "They are a set of web platform APIs that allow you to create new custom, reusable, encapsulated HTML tags to use in web apps.",
                                "Web Components are an outdated technology replaced by modern JavaScript frameworks.",
                                "They are primarily used for server-side rendering of web pages."
                            ],
                            'correct_option': "They are a set of web platform APIs that allow you to create new custom, reusable, encapsulated HTML tags to use in web apps.",
                            'explanation': "Web Components are a set of web platform APIs that allow developers to create new custom, reusable, encapsulated HTML tags (Custom Elements) that can be used natively in any web application, regardless of the JavaScript framework. Key technologies include: 1. Custom Elements: Define new HTML tags. 2. Shadow DOM: Provides encapsulated styling and markup, preventing conflicts. 3. HTML Templates: Define reusable markup structures. Benefits include improved reusability, strong encapsulation, and framework-agnostic interoperability."
                        },
                        {
                            'question': 'Compare and contrast different frontend testing strategies (Unit, Integration, E2E).',
                            'type': 'technical',
                            'context': 'Discuss their purpose, tools, and best practices.',
                            'keywords': ['frontend testing', 'unit testing', 'integration testing', 'e2e testing', 'jest', 'react testing library', 'cypress', 'playwright'],
                            'options': [
                                "All tests should be End-to-End tests for maximum coverage.",
                                "Unit tests check individual components, integration tests verify interactions between components, and End-to-End (E2E) tests simulate user flows across the entire application, each serving different purposes and requiring different tools.",
                                "Testing is not necessary for small frontend applications.",
                                "Testing should only be done manually by QA engineers."
                            ],
                            'correct_option': "Unit tests check individual components, integration tests verify interactions between components, and End-to-End (E2E) tests simulate user flows across the entire application, each serving different purposes and requiring different tools.",
                            'explanation': "Effective frontend testing involves a combination of strategies: 1. Unit Testing: Focuses on individual units of code (functions, components) in isolation (e.g., Jest, React Testing Library). 2. Integration Testing: Verifies that different modules or services work together correctly (e.g., React Testing Library, Cypress). 3. End-to-End (E2E) Testing: Simulates real user scenarios across the entire application, including the UI, backend, and database (e.g., Cypress, Playwright). A balanced testing strategy typically involves a higher number of unit tests, fewer integration tests, and even fewer E2E tests."
                        }
                    ],
                    'system_design': [
                        {
                            'question': 'Design a robust error logging and monitoring system for a high-traffic web application.',
                            'type': 'system_design',
                            'context': 'Consider client-side, server-side, and infrastructure logging.',
                            'keywords': ['error logging', 'monitoring', 'observability', 'sentry', 'splunk', 'prometheus', 'grafana'],
                            'options': [
                                "Only log critical errors manually to a text file.",
                                "Rely solely on browser console errors for debugging production issues.",
                                "Implement client-side error tracking (e.g., Sentry), aggregate server-side logs centrally (e.g., ELK stack, Splunk), set up infrastructure monitoring (Prometheus/Grafana), and define clear alerting rules.",
                                "Disable all logging in production for performance."
                            ],
                            'correct_option': "Implement client-side error tracking (e.g., Sentry), aggregate server-side logs centrally (e.g., ELK stack, Splunk), set up infrastructure monitoring (Prometheus/Grafana), and define clear alerting rules.",
                            'explanation': "A robust error logging and monitoring system is crucial for high-traffic applications. This involves: 1. Client-Side Error Tracking: Using services like Sentry to capture JavaScript errors in the browser. 2. Centralized Server-Side Logging: Aggregating logs from all backend services into a central system (e.g., ELK Stack - Elasticsearch, Logstash, Kibana; or Splunk) for easy searching and analysis. 3. Infrastructure Monitoring: Using tools like Prometheus for metrics collection and Grafana for visualization to monitor server health, resource utilization, and application performance. 4. Alerting: Setting up rules to notify teams proactively about critical errors or performance degradation."
                        },
                        {
                            'question': 'How would you design a microservices architecture for an e-commerce platform?',
                            'type': 'system_design',
                            'context': 'Discuss service decomposition, communication, and data management.',
                            'keywords': ['microservices', 'e-commerce', 'service discovery', 'api gateway', 'event-driven', 'data consistency'],
                            'options': [
                                "Build a single, monolithic application for all functionalities.",
                                "Deploy all services on a single server without isolation.",
                                "Decompose the platform into independent, loosely coupled services (e.g., Product, Order, User), use an API Gateway for external access, implement inter-service communication via REST/gRPC or message queues, and consider eventual consistency for data.",
                                "Avoid using databases in a microservices architecture."
                            ],
                            'correct_option': "Decompose the platform into independent, loosely coupled services (e.g., Product, Order, User), use an API Gateway for external access, implement inter-service communication via REST/gRPC or message queues, and consider eventual consistency for data.",
                            'explanation': "Designing a microservices architecture for an e-commerce platform involves breaking down the application into smaller, independent, and loosely coupled services (e.g., Product Catalog Service, Order Management Service, User Profile Service). Key considerations include: 1. Service Decomposition: Defining clear boundaries for each service. 2. Communication: Services can communicate via synchronous (REST, gRPC) or asynchronous (message queues like Kafka, RabbitMQ) methods. 3. API Gateway: A single entry point for clients to access various services. 4. Data Management: Each service typically owns its data, leading to distributed data and often requiring eventual consistency strategies. 5. Service Discovery: Mechanisms for services to find and communicate with each other dynamically. Benefits include scalability, fault isolation, and independent deployment."
                        },
                        {
                            'question': 'Design a Content Delivery Network (CDN) integration strategy for a global web application.',
                            'type': 'system_design',
                            'context': 'Focus on asset delivery, caching, and invalidation.',
                            'keywords': ['cdn', 'content delivery network', 'caching', 'edge locations', 'asset delivery', 'invalidation', 'global application'],
                            'options': [
                                "Serve all static assets directly from the origin server.",
                                "Only use a CDN for image files, not JavaScript or CSS.",
                                "Integrate a CDN to cache static assets at edge locations globally, reducing latency and origin server load; implement effective caching headers and a clear invalidation strategy for updated content.",
                                "Manually replicate assets to servers in different regions."
                            ],
                            'correct_option': "Integrate a CDN to cache static assets at edge locations globally, reducing latency and origin server load; implement effective caching headers and a clear invalidation strategy for updated content.",
                            'explanation': "Integrating a Content Delivery Network (CDN) for a global web application significantly improves performance and scalability. Key aspects: 1. Edge Locations: CDNs cache static assets (images, CSS, JS) at geographically distributed 'edge' servers closer to users, reducing latency. 2. Reduced Origin Load: Offloads traffic from the origin server, improving its performance. 3. Caching Strategy: Implement appropriate HTTP caching headers (e.g., `Cache-Control`, `Expires`) to control how long assets are cached. 4. Invalidation: A clear strategy for purging or invalidating cached content when assets are updated. 5. Security: CDNs often provide DDoS protection and WAF capabilities."
                        }
                    ],
                    'behavioral': [
                        {
                            'question': 'Describe a time you had to influence a cross-functional team without direct authority.',
                            'type': 'behavioral',
                            'context': 'Focus on your influence strategies and communication skills.',
                            'keywords': ['influence', 'leadership', 'cross-functional', 'communication', 'negotiation', 'persuasion'],
                            'options': [
                                "I demanded that the team follow my instructions.",
                                "I presented my ideas as suggestions and let others decide.",
                                "I built a strong case with data and logic, understood their perspectives, found common ground, and communicated the benefits collaboratively, leading to their buy-in.",
                                "I escalated the issue to senior management immediately."
                            ],
                            'correct_option': "I built a strong case with data and logic, understood their perspectives, found common ground, and communicated the benefits collaboratively, leading to their buy-in.",
                            'explanation': "Influencing without direct authority requires strong communication, empathy, and strategic thinking. Effective approaches include: 1. Building Relationships: Establishing trust and rapport. 2. Data-Driven Arguments: Presenting compelling evidence to support your ideas. 3. Understanding Perspectives: Listening to and addressing the concerns of others. 4. Finding Common Ground: Identifying shared goals or interests. 5. Collaborative Problem-Solving: Working together to find solutions, making others feel heard and valued, which leads to greater buy-in."
                        },
                        {
                            'question': 'How do you handle technical debt in a large codebase?',
                            'type': 'behavioral',
                            'context': 'Discuss identification, prioritization, and strategies for reduction.',
                            'keywords': ['technical debt', 'code quality', 'refactoring', 'prioritization', 'continuous improvement'],
                            'options': [
                                "Ignore technical debt, as it doesn't affect new features.",
                                "Address all technical debt immediately, regardless of impact.",
                                "Identify and quantify technical debt, prioritize based on impact and effort, allocate dedicated time for refactoring (e.g., sprint by sprint), and integrate debt reduction into regular development cycles.",
                                "Only senior developers are responsible for technical debt."
                            ],
                            'correct_option': "Identify and quantify technical debt, prioritize based on impact and effort, allocate dedicated time for refactoring (e.g., sprint by sprint), and integrate debt reduction into regular development cycles.",
                            'explanation': "Managing technical debt is crucial for long-term project health. Strategies include: 1. Identification: Regularly audit codebases for areas of debt (e.g., complex logic, duplication). 2. Quantification: Assess the impact (e.g., increased bugs, slower development) and effort needed to fix. 3. Prioritization: Address high-impact, low-effort debt first. 4. Allocation: Dedicate specific time in sprints for refactoring. 5. Integration: Make debt reduction a continuous part of the development process, not just a one-off task. Tools like static analysis can help identify debt."
                        }
                    ]
                }
            },
            'backend_developer': {
                'entry': {
                    'technical': [
                        {
                            'question': 'Explain the concept of RESTful APIs.',
                            'type': 'technical',
                            'context': 'Focus on principles and HTTP methods.',
                            'keywords': ['rest', 'restful', 'api', 'http methods', 'stateless', 'resources'],
                            'options': [
                                "A strict set of rules for building web applications using only GET requests.",
                                "An architectural style for networked applications that relies on a stateless, client-server communication model, using standard HTTP methods for resource manipulation.",
                                "A framework for creating graphical user interfaces.",
                                "A database management system."
                            ],
                            'correct_option': "An architectural style for networked applications that relies on a stateless, client-server communication model, using standard HTTP methods for resource manipulation.",
                            'explanation': "REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs are stateless, meaning each request from client to server contains all the information needed to understand the request. They leverage standard HTTP methods (GET for retrieving, POST for creating, PUT/PATCH for updating, DELETE for removing) to interact with 'resources' (e.g., users, products) identified by URIs. Key principles include client-server separation, statelessness, cacheability, layered system, and uniform interface."
                        },
                        {
                            'question': 'Write a Python function to connect to a database and execute a simple query.',
                            'type': 'coding',
                            'context': 'Demonstrate basic database interaction.',
                            'keywords': ['python', 'database', 'sql', 'query', 'psycopg2', 'sqlite', 'orm'],
                            'options': [
                                "def connect_and_query(db_name, query): print('Connecting to database...')",
                                "def connect_and_query(db_name, query): pass # Missing implementation",
                                '''def connect_and_query(db_name, query):
    import sqlite3
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results''',
                                "def connect_and_query(db_name, query): return None"
                            ],
                            'correct_option': '''def connect_and_query(db_name, query):
    import sqlite3
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results''',
                            'explanation': "This Python function demonstrates basic database interaction using SQLite. It establishes a connection to the database (`sqlite3.connect`), creates a cursor object, executes the provided SQL query (`cursor.execute`), fetches all results (`cursor.fetchall`), and finally closes the connection. For production applications, it's generally recommended to use parameterized queries to prevent SQL injection vulnerabilities and to manage connections properly (e.g., using connection pools or ORMs like SQLAlchemy)."
                        },
                        {
                            'question': 'Describe common architectural patterns for backend services (e.g., Monolith, Microservices).',
                            'type': 'technical',
                            'context': 'Discuss pros, cons, and use cases for each.',
                            'keywords': ['monolith', 'microservices', 'architecture patterns', 'scalability', 'maintainability', 'deployment'],
                            'options': [
                                "Monoliths are always preferred for large-scale applications.",
                                "Microservices are inherently easier to develop and deploy than monoliths.",
                                "Monoliths are single, tightly coupled units suitable for smaller projects, while microservices decompose applications into independent, loosely coupled services, offering better scalability and fault isolation but increased operational complexity.",
                                "There is no difference between monoliths and microservices."
                            ],
                            'correct_option': "Monoliths are single, tightly coupled units suitable for smaller projects, while microservices decompose applications into independent, loosely coupled services, offering better scalability and fault isolation but increased operational complexity.",
                            'explanation': "Backend architectural patterns influence scalability, maintainability, and development speed. 1. Monolith: A single, unified codebase where all components are tightly coupled. Pros: Simpler to develop and deploy initially. Cons: Can become unwieldy, harder to scale specific parts, technology lock-in. 2. Microservices: Decomposes the application into small, independent services, each running in its own process and communicating via APIs. Pros: Better scalability, fault isolation, technology diversity. Cons: Increased complexity in deployment, monitoring, and data consistency. The choice depends on project scale, team size, and organizational structure."
                        },
                        {
                            'question': 'Explain the concept of database transactions and their ACID properties.',
                            'type': 'technical',
                            'context': 'Focus on data integrity and reliability.',
                            'keywords': ['database transaction', 'acid properties', 'atomicity', 'consistency', 'isolation', 'durability', 'data integrity'],
                            'options': [
                                "Database transactions are only used for read operations.",
                                "ACID properties refer to the cost of database operations.",
                                "A database transaction is a single logical unit of work that must satisfy ACID properties: Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent transactions don't interfere), and Durability (committed changes are permanent).",
                                "Transactions guarantee high performance above all else."
                            ],
                            'correct_option': "A database transaction is a single logical unit of work that must satisfy ACID properties: Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent transactions don't interfere), and Durability (committed changes are permanent).",
                            'explanation': "Database transactions are sequences of operations performed as a single logical unit of work, ensuring data integrity and reliability. They adhere to ACID properties: 1. Atomicity: All operations within a transaction are either fully completed or completely aborted (all or nothing). 2. Consistency: A transaction brings the database from one valid state to another, preserving all defined rules and constraints. 3. Isolation: Concurrent transactions execute independently without interfering with each other's intermediate results. 4. Durability: Once a transaction is committed, its changes are permanent and survive system failures. These properties are fundamental for reliable database systems."
                        },
                        {
                            'question': 'Describe the role of message queues in a backend system.',
                            'type': 'technical',
                            'context': 'Discuss asynchronous communication, decoupling, and scalability.',
                            'keywords': ['message queue', 'rabbitmq', 'kafka', 'asynchronous communication', 'decoupling', 'scalability', 'resilience'],
                            'options': [
                                "Message queues are used for real-time, synchronous communication only.",
                                "They are a type of database for storing temporary data.",
                                "Message queues facilitate asynchronous communication between decoupled services, buffering messages and improving scalability, resilience, and fault tolerance by enabling services to process tasks independently.",
                                "Message queues are primarily used for sending emails."
                            ],
                            'correct_option': "Message queues facilitate asynchronous communication between decoupled services, buffering messages and improving scalability, resilience, and fault tolerance by enabling services to process tasks independently.",
                            'explanation': "Message queues (e.g., RabbitMQ, Apache Kafka) are essential components in distributed backend systems. Their primary roles include: 1. Asynchronous Communication: Services communicate by sending messages to a queue without waiting for an immediate response. 2. Decoupling: Producers and consumers are independent, reducing direct dependencies. 3. Scalability: Systems can handle bursts of traffic by buffering messages and allowing consumers to scale independently. 4. Resilience: Messages persist in the queue until processed, preventing data loss in case of consumer failures. 5. Load Balancing: Messages can be distributed among multiple consumers. They improve overall system resilience and performance."
                        }
                    ],
                    'problem_solving': [
                        {
                            'question': 'How would you debug a common server-side error like a 500 Internal Server Error?',
                            'type': 'problem_solving',
                            'context': 'Discuss steps and tools.',
                            'keywords': ['debugging', 'server error', '500 error', 'logs', 'stack trace', 'monitoring'],
                            'options': [
                                "Restart the server repeatedly until the error disappears.",
                                "Assume it's a network issue and check internet connectivity.",
                                "Check server logs for stack traces, use debugging tools to step through code, verify database connections, and review recent code changes.",
                                "Blame the frontend team without investigation."
                            ],
                            'correct_option': "Check server logs for stack traces, use debugging tools to step through code, verify database connections, and review recent code changes.",
                            'explanation': "Debugging a 500 Internal Server Error on the backend involves: 1. Checking Server Logs: The most crucial step; logs provide stack traces and error messages that pinpoint the exact line of code causing the issue. 2. Reviewing Recent Changes: New deployments or code changes are often the cause. 3. Verifying Dependencies: Ensure database connections, external APIs, and other services are working. 4. Using Debugging Tools: Employing a debugger (e.g., PDB for Python) to step through the code execution. 5. Environment Consistency: Ensuring development and production environments are as similar as possible."
                        },
                        {
                            'question': 'You encounter a performance bottleneck in a backend API endpoint. How would you identify and resolve it?',
                            'type': 'problem_solving',
                            'context': 'Discuss profiling, database optimization, and caching.',
                            'keywords': ['performance bottleneck', 'profiling', 'database optimization', 'caching', 'api optimization', 'monitoring'],
                            'options': [
                                "Add more servers without investigating the cause.",
                                "Immediately rewrite the entire API endpoint from scratch.",
                                "Use profiling tools to pinpoint slow code, optimize database queries (indexing, N+1 issues), implement caching (Redis, Memcached), and consider asynchronous processing for long-running tasks.",
                                "Blame the network speed for slow responses."
                            ],
                            'correct_option': "Use profiling tools to pinpoint slow code, optimize database queries (indexing, N+1 issues), implement caching (Redis, Memcached), and consider asynchronous processing for long-running tasks.",
                            'explanation': "Identifying and resolving backend performance bottlenecks involves: 1. Profiling: Use tools (e.g., Python's `cProfile`, APM tools) to find code sections consuming most time. 2. Database Optimization: Optimize slow SQL queries (add indexes, avoid N+1 queries), consider denormalization. 3. Caching: Implement caching layers (e.g., Redis, Memcached) for frequently accessed data. 4. Asynchronous Processing: Move long-running tasks (e.g., email sending, image processing, report generation) to background queues. 5. Load Testing: Simulate high traffic to identify breaking points. 6. Monitoring: Continuously monitor API response times and resource utilization to detect issues early."
                        },
                        {
                            'question': 'How do you ensure data security and prevent common vulnerabilities (e.g., SQL Injection, XSS) in backend applications?',
                            'type': 'problem_solving',
                            'context': 'Discuss input validation, authentication, and secure coding practices.',
                            'keywords': ['data security', 'vulnerabilities', 'sql injection', 'xss', 'csrf', 'input validation', 'authentication', 'authorization', 'secure coding'],
                            'options': [
                                "Rely solely on firewalls and network security.",
                                "Trust all user input implicitly.",
                                "Implement strict input validation and sanitization, use parameterized queries for database interactions, ensure secure authentication and authorization, and apply security headers and CSRF tokens.",
                                "Store sensitive data in plain text in the database."
                            ],
                            'correct_option': "Implement strict input validation and sanitization, use parameterized queries for database interactions, ensure secure authentication and authorization, and apply security headers and CSRF tokens.",
                            'explanation': "Ensuring backend data security and preventing vulnerabilities requires a multi-layered approach: 1. Input Validation & Sanitization: Never trust user input; validate and sanitize all inputs to prevent injection attacks. 2. SQL Injection: Use parameterized queries (prepared statements) instead of string concatenation for SQL. 3. Cross-Site Scripting (XSS): Sanitize and escape all user-generated content before rendering it on the frontend. 4. Cross-Site Request Forgery (CSRF): Use CSRF tokens. 5. Authentication & Authorization: Implement strong password policies, multi-factor authentication, and granular access controls. 6. Security Headers: Set HTTP security headers (e.g., CSP, X-Content-Type-Options). 7. Regular Security Audits and Penetration Testing."
                        }
                    ],
                    'system_design': [
                        {
                            'question': 'Design a simple URL shortening service.',
                            'type': 'system_design',
                            'context': 'Consider database schema, redirection, and collision handling.',
                            'keywords': ['url shortener', 'system design', 'database schema', 'redirection', 'collision', 'hash'],
                            'options': [
                                "Store full URLs in a text file and manually create short codes.",
                                "Use a simple incrementing counter for short codes, ignoring collisions.",
                                "Design a database schema to store original and shortened URLs, generate unique short codes (e.g., using base62 encoding of an incrementing ID or a hash function), implement efficient redirection, and handle potential hash collisions.",
                                "Store short URLs only in browser cookies."
                            ],
                            'correct_option': "Design a database schema to store original and shortened URLs, generate unique short codes (e.g., using base62 encoding of an incrementing ID or a hash function), implement efficient redirection, and handle potential hash collisions.",
                            'explanation': "Designing a URL shortening service involves: 1. Database Schema: A table to map short codes to original URLs, creation date, click count, etc. 2. Short Code Generation: Can be done by: a) Hashing the original URL (e.g., MD5, SHA256) and taking a portion, or b) Base62 encoding of an incrementing ID. 3. Collision Handling: If using hashing, regenerate or append characters on collision. If using incrementing IDs, uniqueness is guaranteed. 4. Redirection: When a short URL is accessed, retrieve the original URL from the database and perform a 301 (permanent) or 302 (temporary) HTTP redirect. 5. Scalability: Consider distributed databases and caching for high traffic."
                        },
                        {
                            'question': 'How would you design a distributed caching system for a high-volume backend application?',
                            'type': 'system_design',
                            'context': 'Consider caching strategies, consistency, and eviction policies.',
                            'keywords': ['distributed caching', 'caching strategies', 'consistency', 'eviction policies', 'redis', 'memcached', 'cdn'],
                            'options': [
                                "Only cache data on the client-side.",
                                "Store all data in the primary database without any caching.",
                                "Implement a distributed cache (e.g., Redis Cluster, Memcached) with appropriate caching strategies (e.g., cache-aside, write-through), consider consistency models (eventual vs. strong), and define eviction policies (LRU, LFU).",
                                "Use local file system as a distributed cache."
                            ],
                            'correct_option': "Implement a distributed cache (e.g., Redis Cluster, Memcached) with appropriate caching strategies (e.g., cache-aside, write-through), consider consistency models (eventual vs. strong), and define eviction policies (LRU, LFU).",
                            'explanation': "Designing a distributed caching system is crucial for high-volume backend applications. Key considerations: 1. Caching Strategies: a) Cache-Aside: Application retrieves data from cache first, then DB if not found. b) Write-Through: Data written to cache and DB simultaneously. 2. Consistency: Eventual consistency (data becomes consistent over time) vs. Strong consistency (data is immediately consistent). 3. Eviction Policies: How items are removed from cache (e.g., Least Recently Used (LRU), Least Frequently Used (LFU), Time-To-Live (TTL)). 4. Technologies: Redis and Memcached are popular choices for in-memory distributed caches. 5. Scalability: Ensure the caching layer itself is scalable and highly available."
                        },
                        {
                            'question': 'Design a system to handle background jobs and asynchronous tasks in a web application.',
                            'type': 'system_design',
                            'context': 'Consider task queues, workers, and scheduling.',
                            'keywords': ['background jobs', 'asynchronous tasks', 'task queue', 'celery', 'rabbitmq', 'redis', 'workers', 'scheduling'],
                            'options': [
                                "Execute all long-running tasks synchronously within the main request-response cycle.",
                                "Manually run scripts for each background task.",
                                "Implement a task queue (e.g., Celery with RabbitMQ/Redis) where long-running tasks are offloaded to dedicated worker processes, allowing the main application to remain responsive.",
                                "Store background tasks in a local text file."
                            ],
                            'correct_option': "Implement a task queue (e.g., Celery with RabbitMQ/Redis) where long-running tasks are offloaded to dedicated worker processes, allowing the main application to remain responsive.",
                            'explanation': "Handling background jobs and asynchronous tasks is essential for keeping web applications responsive and scalable. Key components: 1. Task Queue: A messaging system (e.g., RabbitMQ, Redis) where tasks are placed. 2. Workers: Separate processes that continuously pull tasks from the queue and execute them. 3. Task Library: A framework (e.g., Celery in Python) that facilitates defining tasks, sending them to the queue, and managing workers. This pattern offloads time-consuming operations (e.g., email sending, image processing, report generation) from the main application thread, improving user experience and system throughput. Scheduling (e.g., cron jobs) can also be integrated for recurring tasks."
                        }
                    ]
                },
                'mid': {
                    'technical': [
                        {
                            'question': 'Explain Infrastructure as Code (IaC) and its benefits (e.g., Terraform, Ansible).',
                            'type': 'technical',
                            'context': 'Discuss automation, versioning, and idempotency.',
                            'keywords': ['iac', 'infrastructure as code', 'terraform', 'ansible', 'cloudformation', 'automation', 'versioning', 'idempotency', 'devops'],
                            'options': [
                                "IaC involves manually provisioning servers.",
                                "IaC is a method of managing hardware infrastructure only.",
                                "IaC is the practice of managing and provisioning infrastructure through code instead of manual processes, offering benefits like automation, version control, consistency, and idempotency.",
                                "IaC is only used for very small projects."
                            ],
                            'correct_option': "IaC is the practice of managing and provisioning infrastructure through code instead of manual processes, offering benefits like automation, version control, consistency, and idempotency.",
                            'explanation': "Infrastructure as Code (IaC) is a DevOps practice that involves managing and provisioning computing infrastructure (e.g., networks, virtual machines, load balancers) through machine-readable definition files, rather than manual hardware configuration or interactive configuration tools. Benefits include: 1. Automation: Automates provisioning and management. 2. Version Control: Infrastructure configurations can be versioned like application code. 3. Consistency: Ensures environments are consistent across development, testing, and production. 4. Idempotency: Applying the same configuration multiple times yields the same result. Popular tools include Terraform, Ansible, AWS CloudFormation, and Azure Resource Manager."
                        }
                    ],
                    'senior': {
                        'system_design': [
                            {
                                'question': 'Design a CI/CD pipeline for a complex microservices application deployed on Kubernetes.',
                                'type': 'system_design',
                                'context': 'Consider multi-stage builds, testing, and progressive delivery.',
                                'keywords': ['ci/cd', 'microservices', 'kubernetes', 'docker', 'jenkins', 'gitlab ci', 'argo cd', 'canary deployment', 'blue/green deployment'],
                                'options': [
                                    "Manually build and deploy each microservice.",
                                    "Use a single pipeline for all services, even if they are unrelated.",
                                    "Implement separate pipelines for each microservice, including stages for multi-stage Docker builds, unit/integration/e2e testing, security scanning, artifact management, and progressive delivery strategies (e.g., Canary, Blue/Green) with GitOps principles.",
                                    "Avoid automated testing in the pipeline to speed up deployments."
                                ],
                                'correct_option': "Implement separate pipelines for each microservice, including stages for multi-stage Docker builds, unit/integration/e2e testing, security scanning, artifact management, and progressive delivery strategies (e.g., Canary, Blue/Green) with GitOps principles.",
                                'explanation': "Designing a CI/CD pipeline for microservices on Kubernetes is complex. Key considerations: 1. Per-Service Pipelines: Each microservice should have its own independent pipeline for faster, isolated deployments. 2. Multi-Stage Docker Builds: Optimize image size and build time. 3. Comprehensive Testing: Integrate unit, integration, and end-to-end tests. 4. Security Scanning: Incorporate vulnerability scanning (SAST/DAST). 5. Artifact Management: Store immutable Docker images in a registry. 6. Progressive Delivery: Implement strategies like Canary deployments (gradually shift traffic) or Blue/Green deployments (new version alongside old) for safe releases. 7. GitOps: Use Git as the single source of truth for declarative infrastructure and application deployment."
                            }
                        ]
                    }
                }
            },
            'data_scientist': {
                'entry': {
                    'technical': [
                        {
                            'question': 'Explain the difference between supervised and unsupervised learning.',
                            'type': 'technical',
                            'context': 'Focus on data types and algorithms.',
                            'keywords': ['supervised learning', 'unsupervised learning', 'labeled data', 'unlabeled data', 'classification', 'regression', 'clustering', 'dimensionality reduction'],
                            'options': [
                                "Supervised learning uses unlabeled data, while unsupervised learning uses labeled data.",
                                "Supervised learning involves training models on labeled datasets to make predictions, while unsupervised learning works with unlabeled data to find patterns and structures.",
                                "Supervised learning is only for classification, and unsupervised learning is only for regression.",
                                "There is no fundamental difference; they are interchangeable terms."
                            ],
                            'correct_option': "Supervised learning involves training models on labeled datasets to make predictions, while unsupervised learning works with unlabeled data to find patterns and structures.",
                            'explanation': "Supervised learning uses labeled data (input features paired with corresponding output labels) to train models that can predict outputs for new, unseen data. Common tasks include classification (predicting categories) and regression (predicting continuous values). Examples: spam detection, housing price prediction. Unsupervised learning works with unlabeled data to discover hidden patterns, structures, or relationships within the data. Common tasks include clustering (grouping similar data points) and dimensionality reduction. Examples: customer segmentation, anomaly detection."
                        },
                        {
                            'question': 'What is overfitting in machine learning and how can it be mitigated?',
                            'type': 'technical',
                            'context': 'Discuss bias-variance tradeoff and regularization.',
                            'keywords': ['overfitting', 'underfitting', 'bias-variance tradeoff', 'regularization', 'cross-validation', 'feature selection', 'early stopping'],
                            'options': [
                                "Overfitting occurs when a model is too simple and cannot capture the underlying patterns in the data.",
                                "Overfitting occurs when a model learns the training data too well, including noise, and performs poorly on unseen data. It can be mitigated by techniques like cross-validation, regularization (L1/L2), increasing training data, feature selection, and early stopping.",
                                "Overfitting only happens in unsupervised learning.",
                                "It is always desirable for a model to overfit the training data."
                            ],
                            'correct_option': "Overfitting occurs when a model learns the training data too well, including noise, and performs poorly on unseen data. It can be mitigated by techniques like cross-validation, regularization (L1/L2), increasing training data, feature selection, and early stopping.",
                            'explanation': "Overfitting is a common problem in machine learning where a model learns the training data too closely, capturing noise and specific patterns that don't generalize well to new, unseen data. This results in high variance and low bias. Mitigation techniques include: 1. Cross-validation: Helps estimate model performance on unseen data. 2. Regularization (L1, L2): Adds a penalty to the loss function to prevent large coefficients. 3. More Training Data: Providing more diverse data. 4. Feature Selection/Engineering: Reducing irrelevant features. 5. Early Stopping: Halting training when performance on a validation set starts to degrade. 6. Ensemble Methods: Combining multiple models to reduce variance."
                        },
                        {
                            'question': 'Explain the key metrics used to evaluate classification models (e.g., Accuracy, Precision, Recall, F1-Score).',
                            'type': 'technical',
                            'context': 'Discuss their meaning and when to use them.',
                            'keywords': ['classification metrics', 'accuracy', 'precision', 'recall', 'f1-score', 'confusion matrix', 'true positive', 'false positive', 'true negative', 'false negative'],
                            'options': [
                                "Accuracy is always the best metric for all classification problems.",
                                "Precision measures the proportion of actual positives correctly identified.",
                                "Accuracy (overall correctness), Precision (true positives among predicted positives), Recall (true positives among actual positives), and F1-Score (harmonic mean of precision and recall) are crucial, chosen based on the problem's class imbalance and cost of false positives/negatives.",
                                "These metrics are only used for regression models."
                            ],
                            'correct_option': "Accuracy (overall correctness), Precision (true positives among predicted positives), Recall (true positives among actual positives), and F1-Score (harmonic mean of precision and recall) are crucial, chosen based on the problem's class imbalance and cost of false positives/negatives.",
                            'explanation': "Evaluating classification models requires more than just accuracy, especially with imbalanced datasets. Key metrics derived from a Confusion Matrix: 1. Accuracy: (TP+TN)/(TP+TN+FP+FN) - overall correctness. 2. Precision: TP/(TP+FP) - proportion of positive identifications that were actually correct. Useful when the cost of false positives is high. 3. Recall (Sensitivity): TP/(TP+FN) - proportion of actual positives that were correctly identified. Useful when the cost of false negatives is high. 4. F1-Score: 2 * (Precision * Recall) / (Precision + Recall) - a harmonic mean, balancing precision and recall. The choice of metric depends on the specific problem and the relative costs of different types of errors."
                        },
                        {
                            'question': 'Describe the process of building and deploying a machine learning model into production.',
                            'type': 'technical',
                            'context': 'Focus on MLOps concepts like versioning, monitoring, and CI/CD.',
                            'keywords': ['mlops', 'machine learning pipeline', 'model deployment', 'model monitoring', 'ci/cd', 'versioning', 'reproducibility'],
                            'options': [
                                "Build a model and then manually transfer it to a production server.",
                                "Deployment only involves saving the model file.",
                                "The process includes data collection/preparation, model training, evaluation, versioning (data, code, models), deployment (e.g., containerization), and continuous monitoring for performance degradation and data drift, often automated via CI/CD pipelines.",
                                "Once a model is deployed, it never needs further maintenance."
                            ],
                            'correct_option': "The process includes data collection/preparation, model training, evaluation, versioning (data, code, models), deployment (e.g., containerization), and continuous monitoring for performance degradation and data drift, often automated via CI/CD pipelines.",
                            'explanation': "Building and deploying ML models to production is an iterative MLOps process: 1. Data Pipeline: Collection, cleaning, feature engineering. 2. Model Training & Evaluation: Select algorithm, train, and evaluate performance. 3. Versioning: Track versions of data, code, and models for reproducibility. 4. Packaging & Containerization: Package the model and its dependencies (e.g., Docker). 5. Deployment: Deploy the containerized model (e.g., Kubernetes, serverless). 6. Monitoring: Continuously monitor model performance (e.g., accuracy, latency, data drift) and infrastructure. 7. CI/CD: Automate the entire pipeline for faster and more reliable updates."
                        }
                    ],
                    'problem_solving': [
                        {
                            'question': 'Given a dataset with missing values, what strategies would you employ for imputation?',
                            'type': 'problem_solving',
                            'context': 'Discuss different imputation techniques and their pros/cons.',
                            'keywords': ['missing data', 'imputation', 'mean imputation', 'median imputation', 'mode imputation', 'knn imputation', 'regression imputation', 'data preprocessing'],
                            'options': [
                                "Delete all rows or columns with missing values.",
                                "Replace all missing values with a fixed constant like zero.",
                                "Strategies include mean/median/mode imputation for simplicity, k-Nearest Neighbors (KNN) imputation for similarity-based filling, or regression imputation for predictive filling, chosen based on data type, distribution, and missingness pattern.",
                                "Only consider missing values if they are less than 1% of the dataset."
                            ],
                            'correct_option': "Strategies include mean/median/mode imputation for simplicity, k-Nearest Neighbors (KNN) imputation for similarity-based filling, or regression imputation for predictive filling, chosen based on data type, distribution, and missingness pattern.",
                            'explanation': "Handling missing data is a crucial step in data preprocessing. Imputation techniques include: 1. Simple Imputation (Mean, Median, Mode): Replace missing values with the mean, median, or mode of the column. Simple but can reduce variance. 2. K-Nearest Neighbors (KNN) Imputation: Fills missing values using the average of the k-nearest neighbors. More sophisticated but computationally intensive. 3. Regression Imputation: Predicts missing values using a regression model trained on other features. 4. Deletion: Remove rows/columns with missing values (only suitable if missingness is minimal and random). The choice depends on the nature of the data and the extent and pattern of missingness."
                        }
                    ],
                    'system_design': [
                        {
                            'question': 'Design a data pipeline for ingesting and processing large volumes of streaming data.',
                            'type': 'system_design',
                            'context': 'Consider data sources, messaging queues, processing engines, and storage.',
                            'keywords': ['data pipeline', 'streaming data', 'kafka', 'spark streaming', 'flink', 'data lake', 'real-time processing'],
                            'options': [
                                "Manually import data from files once a day.",
                                "Store all raw streaming data directly in a relational database.",
                                "Utilize a messaging queue (e.g., Kafka) for ingestion, a distributed processing engine (e.g., Spark Streaming, Flink) for real-time processing and transformation, and store processed data in a data lake or data warehouse.",
                                "Only process data once it has been aggregated for a full month."
                            ],
                            'correct_option': "Utilize a messaging queue (e.g., Kafka) for ingestion, a distributed processing engine (e.g., Spark Streaming, Flink) for real-time processing and transformation, and store processed data in a data lake or data warehouse.",
                            'explanation': "Designing a data pipeline for streaming data involves several components: 1. Data Sources: Where the streaming data originates (e.g., IoT devices, clickstreams). 2. Ingestion Layer: A high-throughput, fault-tolerant messaging queue (e.g., Apache Kafka, Amazon Kinesis) to collect raw data. 3. Stream Processing Engine: A distributed computing framework (e.g., Apache Spark Streaming, Apache Flink) to process, transform, and analyze data in real-time. 4. Storage Layer: A data lake (e.g., S3, HDFS) for raw and processed data, and potentially a data warehouse (e.g., Snowflake, BigQuery) for structured data analysis. 5. Visualization/Reporting: Tools to present insights."
                        }
                    ],
                    'behavioral': [
                        {
                            'question': 'Describe a time you had to present complex data findings to a non-technical audience.',
                            'type': 'behavioral',
                            'context': 'Focus on simplification and effective communication.',
                            'keywords': ['communication', 'data visualization', 'stakeholder management', 'simplification', 'storytelling'],
                            'options': [
                                "Use highly technical jargon to impress them.",
                                "Overwhelm them with all available data points.",
                                "Simplify complex concepts using analogies, focus on key insights and their business impact, use clear visualizations, and encourage questions to ensure understanding.",
                                "Avoid presenting to non-technical audiences."
                            ],
                            'correct_option': "Simplify complex concepts using analogies, focus on key insights and their business impact, use clear visualizations, and encourage questions to ensure understanding.",
                            'explanation': "Presenting complex data to a non-technical audience requires effective communication strategies: 1. Simplify: Break down complex concepts into easily understandable terms and analogies. 2. Focus on Impact: Highlight the key insights and their business implications, rather than technical details. 3. Visualize: Use clear, concise, and compelling data visualizations (charts, graphs) instead of raw numbers. 4. Storytelling: Frame the data within a narrative that resonates with the audience. 5. Engage: Encourage questions and provide opportunities for clarification. 6. Know Your Audience: Tailor your presentation to their level of understanding and interests."
                        }
                    ]
                },
                'mid': {
                    'technical': [
                        {
                            'question': 'Explain ensemble learning methods (e.g., Bagging, Boosting, Stacking).',
                            'type': 'technical',
                            'context': 'Discuss how they improve model performance and their differences.',
                            'keywords': ['ensemble learning', 'bagging', 'boosting', 'stacking', 'random forest', 'gradient boosting', 'model performance', 'bias-variance tradeoff'],
                            'options': [
                                "Ensemble methods only work with decision trees.",
                                "They involve training a single, very complex model.",
                                "Ensemble learning combines multiple models to improve overall performance and robustness. Bagging (e.g., Random Forest) builds independent models and averages predictions. Boosting (e.g., Gradient Boosting) builds sequential models, correcting errors of previous ones. Stacking trains a meta-model on predictions of base models.",
                                "Ensemble methods always increase model complexity without improving accuracy."
                            ],
                            'correct_option': "Ensemble learning combines multiple models to improve overall performance and robustness. Bagging (e.g., Random Forest) builds independent models and averages predictions. Boosting (e.g., Gradient Boosting) builds sequential models, correcting errors of previous ones. Stacking trains a meta-model on predictions of base models.",
                            'explanation': "Ensemble learning combines predictions from multiple individual models to achieve better overall performance and robustness than a single model. 1. Bagging (Bootstrap Aggregating): Builds multiple independent models (e.g., decision trees in Random Forest) on bootstrapped subsets of the data and averages their predictions. Reduces variance. 2. Boosting: Builds models sequentially, with each new model trying to correct the errors of the previous ones (e.g., AdaBoost, Gradient Boosting, XGBoost, LightGBM). Reduces bias. 3. Stacking: Trains a meta-model to make a final prediction based on the predictions of several base models. This approach often achieves higher performance but is more complex."
                        },
                        {
                            'question': 'Discuss the challenges of working with imbalanced datasets in classification and mitigation techniques.',
                            'type': 'technical',
                            'context': 'Focus on evaluation metrics, resampling, and algorithmic approaches.',
                            'keywords': ['imbalanced dataset', 'classification', 'precision', 'recall', 'f1-score', 'resampling', 'oversampling', 'undersampling', 'smote', 'cost-sensitive learning'],
                            'options': [
                                "Imbalanced datasets do not pose a problem for standard classification algorithms.",
                                "Accuracy is the most reliable metric for imbalanced datasets.",
                                "Challenges include models biased towards the majority class and misleading accuracy scores. Mitigation techniques involve using appropriate metrics (Precision, Recall, F1-Score), resampling (oversampling minority, undersampling majority), generating synthetic samples (SMOTE), or using cost-sensitive learning algorithms.",
                                "The only solution is to collect more data for the minority class."
                            ],
                            'correct_option': "Challenges include models biased towards the majority class and misleading accuracy scores. Mitigation techniques involve using appropriate metrics (Precision, Recall, F1-Score), resampling (oversampling minority, undersampling majority), generating synthetic samples (SMOTE), or using cost-sensitive learning algorithms.",
                            'explanation': "Imbalanced datasets (where one class significantly outnumbers others) present challenges in classification: 1. Biased Models: Standard algorithms tend to favor the majority class. 2. Misleading Metrics: High accuracy can be achieved by simply predicting the majority class. Mitigation techniques: 1. Evaluation Metrics: Use Precision, Recall, F1-Score, AUC-ROC instead of accuracy. 2. Resampling: Oversampling (e.g., SMOTE) the minority class or undersampling the majority class. 3. Algorithmic Approaches: Using algorithms designed for imbalanced data (e.g., cost-sensitive learning, ensemble methods like Balanced Random Forest). 4. Collecting More Data: If feasible, acquire more data for the minority class."
                        }
                    ],
                    'system_design': [
                        {
                            'question': 'Design a recommendation system for an e-commerce platform.',
                            'type': 'system_design',
                            'context': 'Consider collaborative filtering, content-based, and hybrid approaches.',
                            'keywords': ['recommendation system', 'collaborative filtering', 'content-based filtering', 'hybrid recommendation', 'e-commerce', 'cold start', 'scalability'],
                            'options': [
                                "Only recommend the most popular items to all users.",
                                "Manually curate all recommendations for each user.",
                                "Implement a hybrid approach combining collaborative filtering (user-item interactions) and content-based filtering (item attributes), addressing cold-start problems, and ensuring scalability for large user bases and item catalogs.",
                                "Store all user preferences in a simple text file."
                            ],
                            'correct_option': "Implement a hybrid approach combining collaborative filtering (user-item interactions) and content-based filtering (item attributes), addressing cold-start problems, and ensuring scalability for large user bases and item catalogs.",
                            'explanation': "Designing a recommendation system involves various approaches: 1. Collaborative Filtering: Recommends items based on user-item interactions (e.g., 'users who liked this also liked...'). Suffers from cold-start problem (new users/items). 2. Content-Based Filtering: Recommends items similar to those a user has liked in the past, based on item attributes. 3. Hybrid Approaches: Combine collaborative and content-based methods to leverage strengths and mitigate weaknesses (e.g., cold start). Key challenges: scalability (for large datasets), real-time recommendations, and addressing bias. Infrastructure often involves distributed processing (Spark) and specialized databases."
                        }
                    ]
                },
                'senior': {
                    'technical': [
                        {
                            'question': 'Discuss MLOps principles and how they are applied in production.',
                            'type': 'technical',
                            'context': 'Cover aspects like model versioning, monitoring, and deployment.',
                            'keywords': ['mlops', 'machine learning operations', 'ci/cd', 'model monitoring', 'model deployment', 'versioning', 'reproducibility'],
                            'options': [
                                "MLOps is only about model training, not deployment.",
                                "It is a manual process of deploying models to production.",
                                "MLOps integrates DevOps principles into machine learning, focusing on automating the ML lifecycle: continuous integration (CI), continuous delivery (CD), continuous training (CT), and continuous monitoring (CM) of models in production, ensuring reproducibility, scalability, and governance.",
                                "MLOps is only for small, experimental ML projects."
                            ],
                            'correct_option': "MLOps integrates DevOps principles into machine learning, focusing on automating the ML lifecycle: continuous integration (CI), continuous delivery (CD), continuous training (CT), and continuous monitoring (CM) of models in production, ensuring reproducibility, scalability, and governance.",
                            'explanation': "MLOps (Machine Learning Operations) extends DevOps principles to the machine learning lifecycle, aiming to streamline and automate the process of taking ML models from experimentation to production and maintenance. Key principles: 1. Continuous Integration (CI): Automating code and data validation. 2. Continuous Delivery (CD): Automating model deployment. 3. Continuous Training (CT): Automatically retraining models based on new data. 4. Continuous Monitoring (CM): Tracking model performance, data drift, and anomalies in production. This ensures reproducibility, scalability, governance, and rapid iteration of ML systems."
                        }
                    ]
                }
            },
            'devops_engineer': {
                'entry': {
                    'technical': [
                        {
                            'question': 'What is Docker and why is it used in DevOps?',
                            'type': 'technical',
                            'context': 'Explain containers and their benefits.',
                            'keywords': ['docker', 'containers', 'devops', 'virtualization', 'portability', 'isolation'],
                            'options': [
                                "Docker is a programming language used for scripting automation.",
                                "Docker is a traditional virtual machine software that creates full operating system copies.",
                                "Docker is a platform for developing, shipping, and running applications in containers, providing lightweight, portable, and isolated environments that ensure consistency across different stages of the development lifecycle.",
                                "Docker is a tool solely for managing databases."
                            ],
                            'correct_option': "Docker is a platform for developing, shipping, and running applications in containers, providing lightweight, portable, and isolated environments that ensure consistency across different stages of the development lifecycle.",
                            'explanation': "Docker is an open-source platform that enables developers to build, ship, and run applications in lightweight, portable, and self-sufficient units called containers. Unlike traditional virtual machines, containers share the host OS kernel, making them more efficient. In DevOps, Docker promotes consistency ('build once, run anywhere'), faster deployment, environment isolation, and simplified dependency management, streamlining the entire software delivery pipeline from development to production."
                        },
                        {
                            'question': 'Explain the difference between Continuous Integration (CI) and Continuous Delivery (CD).',
                            'type': 'technical',
                            'context': 'Focus on automation, testing, and deployment.',
                            'keywords': ['ci', 'cd', 'continuous integration', 'continuous delivery', 'devops', 'automation', 'testing', 'deployment'],
                            'options': [
                                "CI is manual testing, and CD is automated deployment.",
                                "CI is the process of automatically building and testing code changes frequently, while CD is the extension of CI to automatically release validated code to a repository (Continuous Delivery) or directly to production (Continuous Deployment).",
                                "CI only applies to backend development, and CD only to frontend.",
                                "There is no practical difference between CI and CD."
                            ],
                            'correct_option': "CI is the process of automatically building and testing code changes frequently, while CD is the extension of CI to automatically release validated code to a repository (Continuous Delivery) or directly to production (Continuous Deployment).",
                            'explanation': "Continuous Integration (CI) is a DevOps practice where developers frequently merge their code changes into a central repository, followed by automated builds and tests to detect integration errors early. Continuous Delivery (CD) extends CI by ensuring that the codebase is always in a deployable state, automatically releasing validated code to a repository from which it can be manually deployed to production. Continuous Deployment (also CD) takes this a step further by automatically deploying every validated change to production without manual intervention. Together, CI/CD pipelines automate the software delivery lifecycle, improving speed, reliability, and quality."
                        },
                        {
                            'question': 'What is Kubernetes and why is it used for container orchestration?',
                            'type': 'technical',
                            'context': 'Discuss container management, scaling, and self-healing.',
                            'keywords': ['kubernetes', 'k8s', 'container orchestration', 'docker', 'scaling', 'self-healing', 'deployment', 'devops'],
                            'options': [
                                "Kubernetes is a programming language for cloud development.",
                                "Kubernetes is a tool for developing single-container applications.",
                                "Kubernetes is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications, providing features like self-healing, load balancing, and rolling updates.",
                                "Kubernetes is a database management system for large datasets."
                            ],
                            'correct_option': "Kubernetes is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications, providing features like self-healing, load balancing, and rolling updates.",
                            'explanation': "Kubernetes (K8s) is an open-source platform designed to automate the deployment, scaling, and management of containerized applications. It addresses the challenges of running many containers in production by providing: 1. Orchestration: Automates the deployment and management of containerized workloads. 2. Scaling: Automatically scales applications up or down based on demand. 3. Self-healing: Automatically restarts failed containers, replaces unhealthy ones, and reschedules containers on healthy nodes. 4. Load Balancing: Distributes network traffic to ensure stability. 5. Rolling Updates: Enables seamless updates without downtime. Kubernetes is fundamental for managing microservices architectures in cloud-native environments."
                        }
                    ],
                    'problem_solving': [
                        {
                            'question': 'How would you troubleshoot a failed deployment in a CI/CD pipeline?',
                            'type': 'problem_solving',
                            'context': 'Discuss common causes and debugging steps.',
                            'keywords': ['ci/cd', 'deployment failure', 'troubleshooting', 'logs', 'rollback', 'configuration', 'environment', 'networking'],
                            'options': [
                                "Ignore the failure and redeploy repeatedly.",
                                "Assume it's always a code error and revert immediately.",
                                "Examine logs at each stage of the pipeline (build, test, deploy), verify configuration files, check environment variables, test network connectivity to dependencies, and consider a rollback if needed.",
                                "Blame the last developer to commit code."
                            ],
                            'correct_option': "Examine logs at each stage of the pipeline (build, test, deploy), verify configuration files, check environment variables, test network connectivity to dependencies, and consider a rollback if needed.",
                            'explanation': "Troubleshooting failed CI/CD deployments requires a systematic approach: 1. Check Logs: Review build, test, and deployment logs for error messages and stack traces. 2. Verify Configuration: Ensure `Dockerfile`, `CI/CD pipeline scripts`, and environment variables are correct. 3. Environment Consistency: Check if differences between development and production environments are causing issues. 4. Dependencies & Network: Verify connectivity to databases, external services, and internal dependencies. 5. Rollback: If the issue isn't immediately obvious, initiate a rollback to a stable version to minimize downtime. 6. Incremental Deployment: Deploy small changes frequently to isolate issues more easily."
                        }
                    ],
                    'system_design': [
                        {
                            'question': 'Design a highly available and fault-tolerant system architecture.',
                            'type': 'system_design',
                            'context': 'Consider redundancy, load balancing, and disaster recovery.',
                            'keywords': ['high availability', 'fault tolerance', 'redundancy', 'load balancing', 'disaster recovery', 'failover', 'multi-region'],
                            'options': [
                                "Deploy all components on a single server without backups.",
                                "Only focus on reducing costs, ignoring uptime.",
                                "Implement redundancy at all layers (servers, databases), use load balancers for traffic distribution, design for graceful degradation and automatic failover, and establish a robust disaster recovery plan with backups and multi-region deployments.",
                                "Manually restart services whenever they fail."
                            ],
                            'correct_option': "Implement redundancy at all layers (servers, databases), use load balancers for traffic distribution, design for graceful degradation and automatic failover, and establish a robust disaster recovery plan with backups and multi-region deployments.",
                            'explanation': "Designing for high availability (HA) and fault tolerance (FT) ensures continuous operation even with failures. Key principles: 1. Redundancy: Duplicate critical components (servers, databases, network devices) so if one fails, another can take over. 2. Load Balancing: Distribute incoming traffic across multiple instances to prevent single points of failure and improve performance. 3. Failover: Automatic switching to a redundant system upon detecting a failure. 4. Disaster Recovery (DR): Plan for recovering from major outages (e.g., data centers) using backups, replication, and multi-region deployments. 5. Graceful Degradation: System continues to operate with reduced functionality during partial failures. 6. Monitoring & Alerting: Proactive detection of issues."
                        }
                    ]
                },
                'mid': {
                    'technical': [
                        {
                            'question': 'Explain Infrastructure as Code (IaC) and its benefits (e.g., Terraform, Ansible).',
                            'type': 'technical',
                            'context': 'Discuss automation, versioning, and idempotency.',
                            'keywords': ['iac', 'infrastructure as code', 'terraform', 'ansible', 'cloudformation', 'automation', 'versioning', 'idempotency', 'devops'],
                            'options': [
                                "IaC involves manually provisioning servers.",
                                "IaC is a method of managing hardware infrastructure only.",
                                "IaC is the practice of managing and provisioning infrastructure through code instead of manual processes, offering benefits like automation, version control, consistency, and idempotency.",
                                "IaC is only used for very small projects."
                            ],
                            'correct_option': "IaC is the practice of managing and provisioning infrastructure through code instead of manual processes, offering benefits like automation, version control, consistency, and idempotency.",
                            'explanation': "Infrastructure as Code (IaC) is a DevOps practice that involves managing and provisioning computing infrastructure (e.g., networks, virtual machines, load balancers) through machine-readable definition files, rather than manual hardware configuration or interactive configuration tools. Benefits include: 1. Automation: Automates provisioning and management. 2. Version Control: Infrastructure configurations can be versioned like application code. 3. Consistency: Ensures environments are consistent across development, testing, and production. 4. Idempotency: Applying the same configuration multiple times yields the same result. Popular tools include Terraform, Ansible, AWS CloudFormation, and Azure Resource Manager."
                        }
                    ],
                    'senior': {
                        'system_design': [
                            {
                                'question': 'Design a CI/CD pipeline for a complex microservices application deployed on Kubernetes.',
                                'type': 'system_design',
                                'context': 'Consider multi-stage builds, testing, and progressive delivery.',
                                'keywords': ['ci/cd', 'microservices', 'kubernetes', 'docker', 'jenkins', 'gitlab ci', 'argo cd', 'canary deployment', 'blue/green deployment'],
                                'options': [
                                    "Manually build and deploy each microservice.",
                                    "Use a single pipeline for all services, even if they are unrelated.",
                                    "Implement separate pipelines for each microservice, including stages for multi-stage Docker builds, unit/integration/e2e testing, security scanning, artifact management, and progressive delivery strategies (e.g., Canary, Blue/Green) with GitOps principles.",
                                    "Avoid automated testing in the pipeline to speed up deployments."
                                ],
                                'correct_option': "Implement separate pipelines for each microservice, including stages for multi-stage Docker builds, unit/integration/e2e testing, security scanning, artifact management, and progressive delivery strategies (e.g., Canary, Blue/Green) with GitOps principles.",
                                'explanation': "Designing a CI/CD pipeline for microservices on Kubernetes is complex. Key considerations: 1. Per-Service Pipelines: Each microservice should have its own independent pipeline for faster, isolated deployments. 2. Multi-Stage Docker Builds: Optimize image size and build time. 3. Comprehensive Testing: Integrate unit, integration, and end-to-end tests. 4. Security Scanning: Incorporate vulnerability scanning (SAST/DAST). 5. Artifact Management: Store immutable Docker images in a registry. 6. Progressive Delivery: Implement strategies like Canary deployments (gradually shift traffic) or Blue/Green deployments (new version alongside old) for safe releases. 7. GitOps: Use Git as the single source of truth for declarative infrastructure and application deployment."
                            }
                        ]
                    }
                }
            },
            'product_manager': {
                'entry': {
                    'behavioral': [
                        {
                            'question': 'How do you prioritize features for a product roadmap?',
                            'type': 'behavioral',
                            'context': 'Discuss frameworks and considerations.',
                            'keywords': ['prioritization', 'product roadmap', 'value', 'effort', 'impact', 'stakeholders', 'data-driven'],
                            'options': [
                                "Prioritize features based on what is easiest to build first.",
                                "Only consider requests from the highest-ranking executive.",
                                "Use frameworks like RICE (Reach, Impact, Confidence, Effort) or MoSCoW (Must-have, Should-have, Could-have, Won't-have), considering customer value, business goals, technical feasibility, and stakeholder input.",
                                "Prioritize only features that generate immediate revenue, ignoring long-term strategy."
                            ],
                            'correct_option': "Use frameworks like RICE (Reach, Impact, Confidence, Effort) or MoSCoW (Must-have, Should-have, Could-have, Won't-have), considering customer value, business goals, technical feasibility, and stakeholder input.",
                            'explanation': "Prioritizing features for a product roadmap is critical for effective product management. Common frameworks and considerations include: 1. RICE Scoring: Quantifies Reach (how many users), Impact (how much it matters), Confidence (certainty of estimates), and Effort. 2. MoSCoW Method: Categorizes features as Must-have, Should-have, Could-have, Won't-have. Other factors include: customer value, business goals, technical feasibility and dependencies, market trends, competitive landscape, and stakeholder input. A data-driven approach, using analytics and user feedback, is often key."
                        },
                        {
                            'question': 'Describe your process for gathering and synthesizing user feedback.',
                            'type': 'behavioral',
                            'context': 'Discuss methods, tools, and how insights are used.',
                            'keywords': ['user feedback', 'user research', 'customer interviews', 'surveys', 'usability testing', 'feedback analysis', 'product iteration'],
                            'options': [
                                "Only rely on internal team opinions for product direction.",
                                "Collect feedback but don't actively use it for product decisions.",
                                "Employ various methods like user interviews, surveys, usability testing, and analytics; synthesize insights to identify pain points and opportunities, and integrate findings into the product roadmap for continuous iteration.",
                                "Gather feedback only after a product has been fully launched."
                            ],
                            'correct_option': "Employ various methods like user interviews, surveys, usability testing, and analytics; synthesize insights to identify pain points and opportunities, and integrate findings into the product roadmap for continuous iteration.",
                            'explanation': "Gathering and synthesizing user feedback is vital for building user-centric products. A robust process includes: 1. Collection Methods: User interviews, surveys, usability testing, feedback forms, social media monitoring, analytics. 2. Centralization: Store feedback in a structured way (e.g., product management tools). 3. Synthesis: Analyze qualitative and quantitative data to identify patterns, pain points, and opportunities (e.g., affinity mapping, sentiment analysis). 4. Prioritization: Rank insights based on impact and feasibility. 5. Action: Translate insights into actionable items on the product roadmap, ensuring continuous product iteration and improvement."
                        }
                    ],
                    'product_strategy': [
                        {
                            'question': 'How do you define and measure product success?',
                            'type': 'product_strategy',
                            'context': 'Discuss KPIs, OKRs, and alignment with business goals.',
                            'keywords': ['product success', 'kpis', 'okrs', 'north star metric', 'business goals', 'metrics', 'product strategy'],
                            'options': [
                                "Product success is solely determined by the number of features shipped.",
                                "Only financial metrics indicate product success.",
                                "Define clear Key Performance Indicators (KPIs) and Objectives and Key Results (OKRs) aligned with overall business goals; focus on a North Star Metric (e.g., daily active users, customer retention) that reflects core product value.",
                                "Product success is subjective and cannot be measured."
                            ],
                            'correct_option': "Define clear Key Performance Indicators (KPIs) and Objectives and Key Results (OKRs) aligned with overall business goals; focus on a North Star Metric (e.g., daily active users, customer retention) that reflects core product value.",
                            'explanation': "Defining and measuring product success involves establishing clear metrics that align with business objectives. Key components: 1. KPIs (Key Performance Indicators): Quantifiable measures used to track progress toward a business objective (e.g., conversion rate, customer lifetime value). 2. OKRs (Objectives and Key Results): A goal-setting framework where Objectives are ambitious goals and Key Results are measurable outcomes. 3. North Star Metric: A single, critical metric that best captures the core value your product delivers to customers. It should be leading (predictive of future success), measurable, and actionable. Success is not just about features, but about delivering measurable value."
                        }
                    ]
                },
                'mid': {
                    'technical': [
                        {
                            'question': 'Explain the technical concepts behind A/B testing.',
                            'type': 'technical',
                            'context': 'Focus on hypothesis testing, randomization, and statistical significance.',
                            'keywords': ['a/b testing', 'hypothesis testing', 'randomization', 'statistical significance', 'frontend development', 'data analysis'],
                            'options': [
                                "A/B testing is only for backend performance optimization.",
                                "It involves randomly deploying two different versions of a feature without any measurement.",
                                "A/B testing involves comparing two versions (A and B) of a webpage or feature by showing them to different user segments, applying randomization, forming a hypothesis, and using statistical methods to determine which version performs better based on predefined metrics and statistical significance.",
                                "A/B testing requires changing code for every user to see all variations."
                            ],
                            'correct_option': "A/B testing involves comparing two versions (A and B) of a webpage or feature by showing them to different user segments, applying randomization, forming a hypothesis, and using statistical methods to determine which version performs better based on predefined metrics and statistical significance.",
                            'explanation': "A/B testing (or split testing) is a method of comparing two versions of a webpage or app feature against each other to determine which one performs better. Technical concepts: 1. Hypothesis: A clear statement about what you expect to happen. 2. Randomization: Users are randomly assigned to see either version A or B to ensure unbiased results. 3. Metrics: Define key metrics to measure success (e.g., conversion rate, click-through rate). 4. Statistical Significance: Use statistical tests to determine if observed differences are truly significant or due to chance. Tools often manage traffic splitting and data collection."
                        }
                    ],
                    'system_design': [
                        {
                            'question': 'Design a system for feature flagging in a web application.',
                            'type': 'system_design',
                            'context': 'Consider enabling/disabling features, progressive rollout, and A/B testing.',
                            'keywords': ['feature flags', 'feature toggles', 'progressive rollout', 'a/b testing', 'remote configuration', 'deployment'],
                            'options': [
                                "Feature flags require deploying new code for every feature change.",
                                "They are only used for A/B testing, not for toggling features.",
                                "Design a system to remotely enable/disable features for specific users or segments without code deploys, allowing for progressive rollouts, A/B testing, and quick kill switches; requires a configuration service and client-side SDKs.",
                                "Feature flags are only implemented at the network layer."
                            ],
                            'correct_option': "Design a system to remotely enable/disable features for specific users or segments without code deploys, allowing for progressive rollouts, A/B testing, and quick kill switches; requires a configuration service and client-side SDKs.",
                            'explanation': "A feature flagging system allows you to remotely enable or disable features in your application without deploying new code. Key design aspects: 1. Configuration Service: A backend service that stores and serves feature flag states. 2. Client-Side SDKs: Libraries that integrate with your application to read flag states. 3. Targeting Rules: Define which users or segments see which feature variations (e.g., by geography, user ID, percentage rollout). 4. Use Cases: Enables progressive rollouts, A/B testing, kill switches for problematic features, and personalized experiences. It decouples deployment from release, allowing for more agile development."
                        }
                    ]
                },
                'senior': {
                    'product_strategy': [
                        {
                            'question': 'How do you gather competitive intelligence and use it to inform your product strategy?',
                            'type': 'product_strategy',
                            'context': 'Discuss your research methods and how insights translate into action.',
                            'keywords': ['competitive analysis', 'market research', 'product strategy', 'competitive advantage', 'market trends'],
                            'options': [
                                "Only focus on your own product without looking at competitors.",
                                "Gather information from competitors but don't incorporate it into strategy.",
                                "Conduct continuous market research, analyze competitor products (features, pricing, UX), monitor industry trends, and synthesize insights to identify opportunities, threats, and differentiation points to inform and adapt your product strategy.",
                                "Competitive intelligence is only relevant during product launch."
                            ],
                            'correct_option': "Conduct continuous market research, analyze competitor products (features, pricing, UX), monitor industry trends, and synthesize insights to identify opportunities, threats, and differentiation points to inform and adapt your product strategy.",
                            'explanation': "Gathering competitive intelligence is crucial for informing product strategy. Process: 1. Identify Competitors: Direct and indirect. 2. Research Methods: Analyze competitor websites, products, pricing, marketing, app store reviews, public reports, earnings calls. Conduct competitive teardowns. 3. Monitor Trends: Keep an eye on broader market and technology trends. 4. Synthesize: Analyze collected data to identify strengths, weaknesses, opportunities, and threats. Understand competitive advantages and disadvantages. 5. Inform Strategy: Use insights to refine your product roadmap, pricing, positioning, and differentiation strategy. This is an ongoing process, not a one-time event."
                        }
                    ]
                }
            },
            'ux_designer': {
                'entry': {
                    'technical': [
                        {
                            'question': 'Explain the concept of responsive web design and its importance.',
                            'type': 'technical',
                            'context': 'Discuss media queries and flexible layouts.',
                            'keywords': ['responsive design', 'media queries', 'flexible layouts', 'mobile-first', 'user experience'],
                            'options': [
                                "Creating a separate website for each device type.",
                                "Designing web pages that adapt their layout and content to different screen sizes and devices, using techniques like fluid grids, flexible images, and media queries.",
                                "Only designing for desktop screens.",
                                "Using fixed-width layouts for all devices."
                            ],
                            'correct_option': "Designing web pages that adapt their layout and content to different screen sizes and devices, using techniques like fluid grids, flexible images, and media queries.",
                            'explanation': "Responsive web design is an approach to web design that makes web pages render well on a variety of devices and screen sizes. It uses a combination of flexible grids and layouts, images, and an intelligent use of CSS media queries. The goal is to provide an optimal viewing experience—easy reading and navigation with a minimum of resizing, panning, and scrolling—across a wide range of devices (from desktop computer monitors to mobile phones). It's crucial for providing a consistent and accessible user experience in today's multi-device world."
                        }
                    ],
                    'problem_solving': [
                        {
                            'question': 'Explain the difference between UX and UI design.',
                            'type': 'problem_solving',
                            'context': 'Focus on their distinct roles and how they complement each other.',
                            'keywords': ['ux design', 'ui design', 'user experience', 'user interface', 'usability', 'aesthetics', 'interaction design'],
                            'options': [
                                "UX and UI design are interchangeable terms for the same role.",
                                "UX design focuses on the user's overall experience and interaction with a product, while UI design focuses on the visual aesthetics and interactivity of the product's interface.",
                                "UI design happens before UX design in the product development process.",
                                "UX design is only about wireframing, and UI design is only about colors."
                            ],
                            'correct_option': "UX design focuses on the user's overall experience and interaction with a product, while UI design focuses on the visual aesthetics and interactivity of the product's interface.",
                            'explanation': "UX (User Experience) design is the process of creating products that provide meaningful and relevant experiences to users. This involves the entire process of acquiring and integrating the product, including aspects of branding, design, usability, and function. UI (User Interface) design is the process of making interfaces, focusing on visual elements and interactive properties. While distinct, they are interdependent: a great UI can be hampered by poor UX, and a great UX needs a well-designed UI to be effective."
                        }
                    ],
                    'behavioral': [
                        {
                            'question': 'Describe your design process for a new feature.',
                            'type': 'behavioral',
                            'context': 'Walk through the steps from research to implementation.',
                            'keywords': ['design process', 'user research', 'wireframing', 'prototyping', 'usability testing', 'iteration'],
                            'options': [
                                "I start coding the feature immediately without any planning.",
                                "My process involves only creating high-fidelity mockups.",
                                "My design process typically involves user research (understanding needs), ideation (sketching, wireframing), prototyping (low-fidelity to high-fidelity), usability testing, and iterative refinement based on feedback, collaborating closely with development.",
                                "I rely solely on stakeholder requests without validating user needs."
                            ],
                            'correct_option': "My design process typically involves user research (understanding needs), ideation (sketching, wireframing), prototyping (low-fidelity to high-fidelity), usability testing, and iterative refinement based on feedback, collaborating closely with development.",
                            'explanation': "A robust design process for a new feature ensures user-centric and effective solutions. Common steps: 1. User Research: Understand user needs, behaviors, pain points (interviews, surveys). 2. Ideation: Brainstorming, sketching, creating user flows and wireframes. 3. Prototyping: Building interactive prototypes (low-fidelity to high-fidelity). 4. Usability Testing: Validate designs with actual users. 5. Iteration: Refine designs based on feedback and testing results. 6. Handoff: Collaborate with developers during implementation. This iterative process ensures the design evolves with user feedback and technical feasibility."
                        }
                    ]
                },
                'mid': {
                    'technical': [
                        {
                            'question': 'Explain the principles of Gestalt psychology as they apply to UX design.',
                            'type': 'technical',
                            'context': 'Discuss principles like proximity, similarity, and closure.',
                            'keywords': ['gestalt principles', 'ux design', 'proximity', 'similarity', 'closure', 'continuity', 'figure-ground', 'common fate'],
                            'options': [
                                "Gestalt principles are only applicable to graphic design, not UX.",
                                "They are a set of rules for writing CSS.",
                                "Gestalt principles describe how humans naturally perceive objects as organized patterns rather than separate parts. Key principles like proximity (grouping by closeness), similarity (grouping by shared characteristics), and closure (perceiving incomplete shapes as complete) are fundamental for creating intuitive and aesthetically pleasing user interfaces.",
                                "They dictate that all elements on a page must be unique."
                            ],
                            'correct_option': "Gestalt principles describe how humans naturally perceive objects as organized patterns rather than separate parts. Key principles like proximity (grouping by closeness), similarity (grouping by shared characteristics), and closure (perceiving incomplete shapes as complete) are fundamental for creating intuitive and aesthetically pleasing user interfaces.",
                            'explanation': "Gestalt psychology principles explain how the human brain perceives visual elements as a whole rather than discrete parts, which is crucial for UX design. Key principles include: 1. Proximity: Elements close to each other are perceived as a group. 2. Similarity: Elements that share visual characteristics (color, shape, size) are perceived as related. 3. Closure: The tendency to perceive incomplete shapes as complete. 4. Continuity: Elements arranged on a line or curve are perceived as belonging together. 5. Figure-Ground: The ability to distinguish a figure from its background. Applying these principles helps designers create intuitive, organized, and aesthetically pleasing interfaces."
                        }
                    ],
                    'system_design': [
                        {
                            'question': 'Design the user flow for a complex multi-step form (e.g., a checkout process).',
                            'type': 'system_design',
                            'context': 'Consider error handling, progress indication, and user guidance.',
                            'keywords': ['user flow', 'multi-step form', 'checkout process', 'error handling', 'progress indicator', 'user guidance', 'ux design', 'usability'],
                            'options': [
                                "Put all form fields on a single, long page.",
                                "Provide no indication of progress to the user.",
                                "Break down the form into logical steps, provide clear progress indicators (e.g., steppers), offer clear error messages and inline validation, allow users to save progress, and minimize distractions.",
                                "Require users to re-enter all data if they make a mistake."
                            ],
                            'correct_option': "Break down the form into logical steps, provide clear progress indicators (e.g., steppers), offer clear error messages and inline validation, allow users to save progress, and minimize distractions.",
                            'explanation': "Designing a complex multi-step form requires careful attention to user experience. Best practices: 1. Break Down Steps: Divide the form into logical, manageable sections. 2. Progress Indicators: Clearly show users where they are in the process (e.g., progress bars, steppers). 3. Clear Instructions & Guidance: Provide concise labels, help text, and visual cues. 4. Inline Validation & Error Handling: Validate input in real-time and provide clear, actionable error messages. 5. Save & Continue: Allow users to save their progress and return later. 6. Minimize Distractions: Keep the UI clean and focused. 7. Mobile Responsiveness: Ensure usability on smaller screens."
                        }
                    ]
                }
            }
        }

    def generate_questions(self, role: str, level: str, focus: str) -> List[Dict]:
        """Generate a set of quiz questions based on role, level, and focus area."""
        if not all([role, level, focus]):
            raise ValueError("Role, level, and focus area are required")
        
        # Get questions for the specified role, level, and focus
        role_questions = self.questions_db.get(role, {})
        level_questions = role_questions.get(level, {})
        focus_questions = level_questions.get(focus, [])
        
        if not focus_questions:
            raise ValueError(f"No questions available for {role} - {level} - {focus}")
        
        # Always return exactly 20 questions
        # If we have fewer than 20 questions, we'll repeat some questions
        # If we have more than 20 questions, we'll randomly select 20
        if len(focus_questions) < 20:
            # Repeat questions to reach 20
            selected_questions = focus_questions * (20 // len(focus_questions) + 1)
            selected_questions = selected_questions[:20]
        else:
            # Randomly select 20 questions
            selected_questions = random.sample(focus_questions, 20)
        
        return selected_questions

    def analyze_answer(self, audio_file_path, question, role, level):
        """Analyze an interview answer with enhanced feedback."""
        try:
            # Convert audio to text
            with sr.AudioFile(audio_file_path) as source:
                audio_data = self.recognizer.record(source)  # read the entire audio file
            text = self.recognizer.recognize_google(audio_data)
            
            # Find question in database
            question_details = self._find_question_details(question, role, level)
            if not question_details:
                return {'error': 'Question not found in database'}, 404
            
            # Comprehensive analysis
            analysis = {
                'transcript': text,
                'keyword_analysis': self._analyze_keyword_coverage(text, question_details['keywords']),
                'length_analysis': self._analyze_answer_length(text, question_details['expected_length']),
                'sentiment_analysis': self.nlp_processor.analyze_sentiment(text),
                'structure_analysis': self._analyze_answer_structure(text),
                'feedback': self._generate_comprehensive_feedback(text, question_details),
                'score': self._calculate_overall_score(text, question_details)
            }
            
            # Save to interview history
            self._save_to_history(analysis, question, role, level)
            
            return analysis
            
        except sr.UnknownValueError:
            return {'error': 'Could not understand audio'}, 400
        except sr.RequestError as e:
            return {'error': f'Could not request results from Google Speech Recognition service; {e}'}, 500
        except Exception as e:
            return {'error': f'An unexpected error occurred during audio processing: {e}'}, 500

    def process_quiz_answer(self, question_text, selected_option, role, level):
        """Process a quiz answer and return correctness and explanation."""
        question_details = self._find_question_details(question_text, role, level)
        if not question_details:
            return {'error': 'Question not found in database'}, 404

        is_correct = (selected_option == question_details['correct_option'])

        # Prepare analysis for history and frontend
        analysis = {
            'question': question_text,
            'selected_option': selected_option,
            'correct_option': question_details['correct_option'],
            'is_correct': is_correct,
            'explanation': question_details['explanation']
        }

        # Generate comprehensive feedback and score
        feedback = self._generate_comprehensive_feedback(selected_option, question_details)
        score = self._calculate_overall_score(selected_option, question_details)

        analysis['feedback'] = feedback
        analysis['score'] = score
        
        # Save to interview history (adapt to quiz format)
        self._save_to_history(analysis, question_text, role, level)

        return analysis

    def _find_question_details(self, question, role, level):
        """Find question details in the database."""
        if role not in self.questions_db or level not in self.questions_db[role]:
            return None
            
        for category in self.questions_db[role][level].values():
            for q in category:
                if q['question'] == question:
                    return q
        return None

    def _analyze_keyword_coverage(self, text, keywords):
        """Enhanced keyword coverage analysis."""
        text_lower = text.lower()
        covered_keywords = [keyword for keyword in keywords if keyword in text_lower]
        missing_keywords = [k for k in keywords if k not in covered_keywords]
        
        # Calculate weighted coverage (more important keywords have higher weight)
        keyword_weights = {k: 1 for k in keywords}  # Can be customized per keyword
        total_weight = sum(keyword_weights.values())
        covered_weight = sum(keyword_weights[k] for k in covered_keywords)
        
        return {
            'covered_keywords': covered_keywords,
            'missing_keywords': missing_keywords,
            'coverage_percentage': (covered_weight / total_weight) * 100,
            'keyword_frequency': {k: text_lower.count(k) for k in covered_keywords}
        }

    def _analyze_answer_length(self, text, expected_length):
        """Enhanced answer length analysis."""
        words = text.split()
        word_count = len(words)
        estimated_minutes = word_count / 150  # Assuming 150 words per minute
        
        length_score = 1 - abs(estimated_minutes - expected_length) / expected_length
        length_score = max(0, min(1, length_score))  # Normalize between 0 and 1
        
        return {
            'word_count': word_count,
            'estimated_minutes': round(estimated_minutes, 1),
            'expected_minutes': expected_length,
            'length_score': round(length_score * 100, 1)
        }

    def _analyze_answer_structure(self, text):
        """Analyze the structure and organization of the answer."""
        sentences = text.split('.')
        structure_indicators = {
            'introduction': ['first', 'to begin', 'initially', 'starting with'],
            'main_points': ['second', 'third', 'additionally', 'furthermore', 'moreover'],
            'examples': ['for example', 'such as', 'specifically', 'in particular'],
            'conclusion': ['finally', 'in conclusion', 'to summarize', 'overall']
        }
        
        structure_scores = {}
        for category, indicators in structure_indicators.items():
            score = sum(1 for sentence in sentences if any(ind in sentence.lower() for ind in indicators))
            structure_scores[category] = min(score / 2, 1)  # Normalize to 0-1
        
        return {
            'structure_scores': structure_scores,
            'overall_structure_score': round(sum(structure_scores.values()) / len(structure_scores) * 100, 1)
        }

    def _generate_comprehensive_feedback(self, text, question_details):
        """Generate detailed feedback on the answer."""
        feedback = {
            'strengths': [],
            'areas_for_improvement': [],
            'specific_suggestions': []
        }
        
        # Analyze keyword coverage
        keyword_analysis = self._analyze_keyword_coverage(text, question_details['keywords'])
        if keyword_analysis['coverage_percentage'] > 70:
            feedback['strengths'].append("Good coverage of key concepts!")
        else:
            feedback['areas_for_improvement'].append(
                f"Consider incorporating more key concepts. Missing: {', '.join(keyword_analysis['missing_keywords'][:3])}"
            )
        
        # Analyze length
        expected_length_val = question_details.get('expected_length', 1) # Default to 1 if not present
        length_analysis = self._analyze_answer_length(text, expected_length_val)
        if length_analysis['length_score'] < 60:
            if length_analysis['estimated_minutes'] < expected_length_val:
                feedback['areas_for_improvement'].append("Your answer could be more detailed. Try to elaborate on your points.")
            else:
                feedback['areas_for_improvement'].append("Your answer is quite long. Try to be more concise while maintaining clarity.")
        
        # Analyze structure
        structure_analysis = self._analyze_answer_structure(text)
        if structure_analysis['overall_structure_score'] < 60:
            feedback['specific_suggestions'].append(
                "Consider structuring your answer with a clear introduction, main points, and conclusion."
            )
        
        # Add role-specific feedback
        if question_details['type'] == 'technical':
            if 'example' not in text.lower() and 'for instance' not in text.lower():
                feedback['specific_suggestions'].append(
                    "For technical questions, try to include specific examples or use cases."
                )
        
        return feedback

    def _calculate_overall_score(self, text, question_details):
        """Calculate overall answer score."""
        # Get individual component scores
        keyword_analysis = self._analyze_keyword_coverage(text, question_details['keywords'])
        expected_length_val = question_details.get('expected_length', 1) # Default to 1 if not present
        length_analysis = self._analyze_answer_length(text, expected_length_val)
        structure_analysis = self._analyze_answer_structure(text)
        sentiment_score = self.nlp_processor.analyze_sentiment(text)
        
        # Weight the components
        weights = {
            'keyword_coverage': 0.4,
            'length': 0.2,
            'structure': 0.2,
            'sentiment': 0.2
        }
        
        # Calculate weighted score
        overall_score = (
            keyword_analysis['coverage_percentage'] * weights['keyword_coverage'] +
            length_analysis['length_score'] * weights['length'] +
            structure_analysis['overall_structure_score'] * weights['structure'] +
            sentiment_score * 100 * weights['sentiment']
        )
        
        return round(overall_score, 1)

    def _save_to_history(self, analysis, question, role, level):
        """Save interview answer analysis to history with enhanced metadata."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'interview_{timestamp}.json'
        filepath = os.path.join(self.interview_history_dir, filename)
        
        history_entry = {
            'timestamp': timestamp,
            'role': role,
            'level': level,
            'question': question,
            'analysis': analysis
        }
        
        with open(filepath, 'w') as f:
            json.dump(history_entry, f, indent=2)

    def get_interview_history(self, role=None, level=None):
        """Retrieve filtered interview history."""
        history = []
        for filename in os.listdir(self.interview_history_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.interview_history_dir, filename), 'r') as f:
                    entry = json.load(f)
                    if (role is None or entry['role'] == role) and \
                       (level is None or entry['level'] == level):
                        history.append(entry)
        
        return sorted(history, key=lambda x: x['timestamp'], reverse=True) 