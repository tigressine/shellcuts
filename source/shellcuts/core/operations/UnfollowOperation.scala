package shellcuts.core.operations

import shellcuts.core.actions.PrintLineAction
import shellcuts.core.structures.{
  Command,
  Configuration,
  Shellcut
}

object UnfollowOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Configuration] = {

    if (parameters.length == 0) {
      Right(Configuration(configuration.crumb, None, configuration.shellcuts))
    } else {
      val originalShellcut = configuration.shellcuts find {
        (shellcut) => shellcut.name == parameters(0)
      }

      if (originalShellcut.isEmpty) {
        return Left(s"""no shellcut with the name "${parameters(0)}"""")
      }

      val newShellcut = Shellcut(
        originalShellcut.get.name,
        None,
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

    if (parameters.length == 0) {
      Right(Command(PrintLineAction, List("default follow command removed")))
    } else {
      Right(
        Command(
          PrintLineAction,
          List(s"""follow command removed for shellcut "${parameters(0)}"""")
        )
      )
    }
  }
}
