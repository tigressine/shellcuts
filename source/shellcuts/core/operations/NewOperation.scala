package shellcuts.core.operations

import shellcuts.core.structures.{
  Configuration,
  Shellcut
}

object NewOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, Configuration] = {

    if (parameters.length < 1) {
      return Left("no name provided for new shellcut")
    }

    if (properties.length < 2) {
      return Left(
        "working directory and/or home directory could not be determined"
      )
    }

    val newShellcut = Shellcut(
      parameters(0),
      parameters.lift(1),
      List(properties(1))
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

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]
  ): Either[String, String] = {

    Right(s"""printf 'new shellcut "${parameters(0)}" created\n'""")
  }
}
