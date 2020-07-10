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

    val prompt = """
      |Usage: $ sc [-F/--FLAG] [SHELLCUT [FOLLOW...]]

      |Examples:
      |  Create a new shellcut for the current directory:
      |    $ sc -n example

      |  Jump to the example location:
      |    $ sc example

      |  Remove the example shellcut:
      |    $ sc -d example

      |  List all available shellcuts:
      |    $ sc -l

      |  See the manpage for more information and examples:
      |    $ man sc
      |""".stripMargin.replaceFirst("\n", "").dropRight(1)

    Right(Command(Action.PrintLine, List(prompt)))
  }
}
