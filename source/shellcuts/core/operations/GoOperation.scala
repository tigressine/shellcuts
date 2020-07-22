package shellcuts.core.operations

import shellcuts.core.actions.{
  JumpAction,
  JumpAndFollowAction
}
import shellcuts.core.structures.{
  Command,
  Configuration
}

object GoOperation extends Operation {
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

    val shellcut = configuration.shellcuts find {
      (shellcut) => shellcut.name == parameters(0)
    }

    if (shellcut.isEmpty) {
      return Left(s"""no shellcut named "${parameters(0)}"""")
    }

    if (shellcut.get.follow.isEmpty && configuration.defaultFollow.isEmpty) {
        return Right(Command(JumpAction, List(shellcut.get.path)))
    }

    if (shellcut.get.follow.isEmpty) {
      Right(
        Command(
          JumpAndFollowAction,
          List(shellcut.get.path, configuration.defaultFollow.get)
        )
      )
    } else {
      Right(
        Command(
          JumpAndFollowAction,
          List(shellcut.get.path, shellcut.get.follow.get)
        )
      )
    }
  }
}
