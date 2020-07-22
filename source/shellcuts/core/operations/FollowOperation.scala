package shellcuts.core.operations

import shellcuts.core.actions.PrintLineAction
import shellcuts.core.structures.{
  Command,
  Configuration,
  Shellcut
}

object FollowOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Configuration] = {

    if (parameters.length == 0) {
      Left("no follow command provided")
    } else if (parameters.length == 1) {
      Right(
        Configuration(
          configuration.crumb,
          Some(parameters(0)),
          configuration.shellcuts
        )
      )
    } else {
      val originalShellcut = configuration.shellcuts find {
        (shellcut) => shellcut.name == parameters(0)
      }

      if (originalShellcut.isEmpty) {
        return Left(s"""no shellcut with the name "${parameters(0)}"""")
      }

      val newShellcut = Shellcut(
        originalShellcut.get.name,
        Some(parameters(1)),
        originalShellcut.get.path
      )

      val filteredShellcuts = configuration.shellcuts filter {
        (shellcut) => shellcut.name != parameters(0)
      } toList

      Right(
        Configuration(
          configuration.crumb,
          configuration.defaultFollow,
          newShellcut :: filteredShellcuts
        )
      )
    }
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Command] = {

    if (parameters.length == 1) {
      Right(Command(PrintLineAction, List("default follow command updated")))
    } else {
      Right(
        Command(
          PrintLineAction,
          List(s"""follow command updated for shellcut "${parameters(0)}"""")
        )
      )
    }
  }
}
