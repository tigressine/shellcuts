package shellcuts.core

import shellcuts.core.operations.Operation

object Parsing {
  val FlagPattern = "(--?[a-zA-Z0-9\\-]*)".r

  // Retrieve the appropriate operation for given commandline arguments.
  def parse(
    crumbOperation: Operation,
    goOperation: Operation,
    helpOperation: Operation,
    operations: Map[String, Operation]
  )(
    arguments: Array[String]
  ): (Operation, List[String]) = {

    arguments.headOption match {
      case None => (crumbOperation, List())
      case Some(argument) => argument match {
        case FlagPattern(flag) => {
          if (operations.contains(flag)) {
            (operations(flag), arguments.slice(1, arguments.length).toList)
          } else {
            (helpOperation, arguments.toList)
          }
        }
        case _ => (goOperation, arguments.toList)
      }
    }
  }
}
