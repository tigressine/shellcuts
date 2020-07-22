package shellcuts.core.operations

import shellcuts.core.actions.PrintLineAction
import shellcuts.core.structures.{
  Command,
  Configuration,
  Shellcut
}

object MoveOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Configuration] = {

    if (parameters.length < 1) {
      return Left("no shellcut name provided")
    }

    if (properties.length < 1) {
      return Left("working directory could not be determined")
    }

    val originalShellcut = configuration.shellcuts find {
      (shellcut) => shellcut.name == parameters(0)
    }

    if (originalShellcut.isEmpty) {
      return Left(s"""no shellcut with the name "${parameters(0)}"""")
    }

    val movedShellcut = Shellcut(
      originalShellcut.get.name,
      originalShellcut.get.follow,
      properties(1)
    )

    val filteredShellcuts = configuration.shellcuts filter {
      (shellcut) => shellcut.name != parameters(0)
    } toList

    Right(
      Configuration(
        configuration.crumb,
        configuration.defaultFollow,
        movedShellcut :: filteredShellcuts
      )
    )
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Command] = {

    Right(
      Command(
        PrintLineAction,
        List(s"""shellcut "${parameters(0)}" moved""")
      )
    )
  }
}
