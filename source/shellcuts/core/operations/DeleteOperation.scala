package shellcuts.core.operations

import shellcuts.core.{
  Configuration,
  Operation
}

object DeleteOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration] = {

    if (parameters.length < 1) {
      Left("Missing shellcut name.")
    } else {
      Right(
        Configuration(
          configuration.crumb,
          configuration.defaultFollow,
          configuration.shellcuts filter {
            (shellcut) => shellcut.name != parameters(0)
          } toList
        )
      )
    }
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String = {

    "delete"
  }
}
