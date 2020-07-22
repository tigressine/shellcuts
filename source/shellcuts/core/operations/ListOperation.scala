package shellcuts.core.operations

import shellcuts.core.actions.PrintLineAction
import shellcuts.core.structures.{
  Command,
  Configuration,
  Shellcut
}

object ListOperation extends Operation {
  val Padding = 3

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

    if (parameters.length > 0) {
      val shellcut = configuration.shellcuts find {
        (shellcut) => shellcut.name == parameters(0)
      }

      if (shellcut.isEmpty) {
        return Left(s"""no shellcut with the name "${parameters(0)}"""")
      }

      if (shellcut.get.follow.isEmpty) {
        Right(
          Command(
            PrintLineAction,
            List(shellcut.get.name + (" " * Padding) + shellcut.get.path)
          )
        )
      } else {
        Right(
          Command(
            PrintLineAction,
            List(
              shellcut.get.name +
              (" " * Padding) +
              shellcut.get.path +
              (" " * Padding) +
              shellcut.get.follow.get
            )
          )
        )
      }
    } else {
      val widestShellcut = configuration.shellcuts maxBy {
        (shellcut) => shellcut.name.length
      }

      Right(
        Command(
          PrintLineAction,
          configuration.shellcuts map {
            (shellcut) => {
              val paddedName = String.format(
                s"%-${widestShellcut.name.length}s", shellcut.name
              )

              paddedName + (" " * Padding) + shellcut.path
            }
          }
        )
      )
    }
  }
}
