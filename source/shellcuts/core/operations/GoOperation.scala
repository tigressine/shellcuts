package shellcuts.core.operations

import shellcuts.core.structures.Configuration

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
  ): Either[String, String] = {

    val shellcut = configuration.shellcuts find {
      (shellcut) => shellcut.name == parameters(0)
    }

    if (shellcut.isEmpty) {
      Left(s"""no shellcut named "${parameters(0)}"""")
    } else {
      val follow = if (shellcut.get.follow.isEmpty) {
        if (configuration.defaultFollow.isEmpty) {
          ""
        } else {
          configuration.defaultFollow.get
        }
      } else {
        shellcut.get.follow.get
      }

      Right(s"""cd '${shellcut.get.paths(0)}'; ${follow}""")
    }
  }
}
