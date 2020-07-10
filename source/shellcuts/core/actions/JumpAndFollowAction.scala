package shellcuts.core.actions

object JumpAndFollowAction extends Action {
  override def posixFormat(arguments: List[String]): Either[String, String] = {
    if (arguments.length < 1) {
      Left("could not format command, no argument provided")
    } else if (arguments.length < 2) {
      Left("could not format command, missing follow-up arguments")
    } else {
      val path = arguments(0).replace("'", "'\\''")

      Right(s"cd '${path}'; ${arguments.drop(1).mkString(" ")}")
    }
  }
}
