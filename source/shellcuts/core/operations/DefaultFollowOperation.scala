package shellcuts.core.operations

import shellcuts.core.{
  Configuration,
  Operation
}

object DefaultFollowOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration] = {

    if (parameters.length < 1) {
      Left("Missing follow command.")
    } else {
      Right(
        Configuration(
          configuration.crumb,
          Some(parameters(0)),
          configuration.shellcuts
        )
      )
    }
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String = {

    "defaultfollow"
  }
}
