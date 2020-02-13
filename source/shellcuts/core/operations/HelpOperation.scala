package shellcuts.core.operations

import shellcuts.core.{
  Configuration,
  Operation
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
  ): String = {

    "help"
  }
}
