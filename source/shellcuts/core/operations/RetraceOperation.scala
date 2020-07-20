package shellcuts.core.operations

import shellcuts.core.actions.{
  JumpAction,
  JumpAndFollowAction
}
import shellcuts.core.structures.{
  Command,
  Configuration
}

object RetraceOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Configuration] = {

    Right(configuration)
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Command] = {

    if (configuration.crumb.isEmpty) {
      return Left("no crumb was available")
    }

    if (configuration.defaultFollow.isEmpty) {
      Right(Command(JumpAction, List(configuration.crumb.get)))
    } else {
      Right(
        Command(
          JumpAndFollowAction,
          List(configuration.crumb.get, configuration.defaultFollow.get)
        )
      )
    }
  }
}
