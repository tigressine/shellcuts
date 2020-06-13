package shellcuts.core.operations

import shellcuts.core.structures.{
  Action,
  Command,
  Configuration
}

object HelpOperation extends Operation {
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

    Right(Command(Action.PrintLine, List("help")))
  }
}
