package shellcuts.core.operations

import shellcuts.core.{
  Configuration,
  Operation,
  Shellcut
}

object NewOperation extends Operation {
  override def modify(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    Either[String, Configuration] = {

    if (parameters.length < 3) {
      return Left("No params")
    }

    val shellcut = Shellcut(
      parameters(0),
      Option(parameters(1)),
      List(parameters(2))
    )
    val shellcuts = configuration.shellcuts filter {
      (shellcut) => shellcut.name != parameters(0)
    } toList

    Right(
      Configuration(
        configuration.crumb,
        configuration.defaultFollow,
        shellcut :: shellcuts
      )
    )
  }

  override def command(
    configuration: Configuration,
    properties: List[String],
    parameters: List[String]):
    String = {

    "gooble"
  }
}
