package shellcuts.core

object Parsing {
  val FlagPattern = "(--?[a-zA-Z0-9\\-]*)".r

  def parse(defaultOperation: Operation,
            unknownOperation: Operation,
            helpOperation: Operation,
            operations: Map[String, Operation])
           (arguments: Array[String]):
           (Operation, List[String]) = {

    arguments.headOption match {
      case None => (defaultOperation, List())
      case Some(argument) => argument match {
        case FlagPattern(flag) => {
          if (operations.contains(flag)) {
            (operations(flag), arguments.slice(1, arguments.length).toList)
          } else {
            (helpOperation, arguments.toList)
          }
        }
        case _ => (unknownOperation, arguments.toList)
      }
    }
  }
}
