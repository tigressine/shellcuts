package shellcuts.core.operations

import shellcuts.core.actions.PrintLineAction
import shellcuts.core.structures.{
  Command,
  Configuration,
  Shellcut
}

object CrumbOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Configuration] = {

    if (properties.length < 2) {
      return Left("working directory could not be determined")
    }

    Right(
      Configuration(
        properties.lift(1),
        configuration.defaultFollow,
        configuration.shellcuts
      )
    )
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Command] = {

    Right(Command(PrintLineAction, List("crumb added for this location")))
  }
}
