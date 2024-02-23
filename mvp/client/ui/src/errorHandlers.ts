export function jsErrorHandler(message: Event | string, source?: string, line?: number, column?: number, error?: Error) {
  reportError({ message, source, line, column }, error)
  alert((error?.name == 'SyntaxError' ? 'Your browser is probably too old, please update:' : 'Technical error occurred, please reload the page:') + '\n' + message)
}

export function reportError(body: object, error?: Error) {
  console.warn("Error reporting logic goes here...");
}

export function handleUnhandledRejection(event: PromiseRejectionEvent) {
  const e: Error & { statusCode: number } | undefined = event.reason
  console.error(e)
  if (e?.stack) return jsErrorHandler(e.message, undefined, undefined, undefined, e)
}

export function initErrorHandlers() {
  window.onerror = jsErrorHandler
  window.addEventListener('unhandledrejection', handleUnhandledRejection)
}
