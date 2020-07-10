package shellcuts.core.actions

object JumpAction extends Action {
  override def posixFormat(arguments: List[String]): Either[String, String] = {
    if (arguments.length < 1) {
      Left("could not format command, no argument provided")
    } else {
      Right(s"cd '${arguments(0).replace("'", "'\\''")}'")
    }
  }
}
