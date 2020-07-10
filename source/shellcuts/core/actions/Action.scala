package shellcuts.core.actions

trait Action {
  def posixFormat(arguments: List[String]): Either[String, String]
}
