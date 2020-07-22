package shellcuts.core.operations

import shellcuts.core.actions.PrintLineAction
import shellcuts.core.structures.{
  Command,
  Configuration
}

object VersionOperation extends Operation {
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

    Right(
      Command(
        PrintLineAction,
        List("shellcuts v1.4.0, 2017 - 2020, written by Tiger Sachse")
      )
    )
  }
}
