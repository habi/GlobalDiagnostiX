<?xml version="1.0" encoding="UTF-8"?><!-- DWXMLSource="NEW_PROD-REV1-DEV.ldat" -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Aptina Imaging <xsl:value-of select="sensor/@part_number"/>-<xsl:value-of select="sensor/@version_name"/></title>
</head>
<body>
  <div style="float:left;display:block;font-weight:normal;font-family:Geneva, Arial, Helvetica, sans-serif;">
	<h1 style="font-size:20px;line-height:20px;">
	<span style="vertical-align:super">
       <xsl:text>&#160;</xsl:text>Aptina Imaging<xsl:text>&#160;&#160;&#160;&#160;</xsl:text><xsl:value-of select="concat(sensor/@part_number,'&#160;&#160;')"/><xsl:value-of select="concat('&#160;&#160;',sensor/@version_name)"/>
	</span></h1>
   	
    <h2 style="font-size:16px;line-height:16px;">&#160;Register/Bitfield Long Descriptions</h2>
    <p style="font-size:11px;line-height:11px;">&#160;Note that items displayed in <font color="#FF0000"><b>Red</b></font> indicate their contents are Confidential, items displayed in <font color="#000000"><b>Black</b></font> indicate their contents are NDA, and items displayed in <font color="#009933"><b>Green</b></font> indicate their contents are Public.</p>
	<table border="0" cellspacing="0" cellpadding="2" style="font-size:11px;">
 	<xsl:call-template name="Display_Reg_Header"/>
 	<xsl:call-template name="Display_Reg_Row">
		<xsl:with-param name="Reg_Nodes" select="sensor/registers/reg"/>
    </xsl:call-template>
    </table><br /><br />
  	  
<br /></div>
</body>
</html>
</xsl:template>


<xsl:template name="Display_Reg_Header">
      <tr bgcolor="#9acd32" align="left">
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Register Name</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Long Description</th>
      </tr>
</xsl:template>

<xsl:template name="Display_Reg_Row">
   <xsl:param name="Reg_Nodes"/>
   <xsl:for-each select="$Reg_Nodes">
      <xsl:choose>
         <xsl:when test="@confidential != ''">
			<xsl:choose>
				<xsl:when test="@confidential = 'Y'">
					<xsl:call-template name="Format_Red_Row"/>
				</xsl:when>
				<xsl:otherwise>
				   <xsl:call-template name="Format_Green_Row"/>
				</xsl:otherwise>
			</xsl:choose>			
         </xsl:when>
         <xsl:otherwise>
           <xsl:call-template name="Format_Black_Row"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:call-template name="Display_Bit_Row">
	     <xsl:with-param name="Bit_Nodes" select="bitfield"/>
      </xsl:call-template>
   </xsl:for-each>
</xsl:template>

<xsl:template name="Display_Bit_Row">
   <xsl:param name="Bit_Nodes"/>  
   <xsl:for-each select="$Bit_Nodes">
      <xsl:choose>
         <xsl:when test="@confidential != ''">
			<xsl:choose>
				<xsl:when test="@confidential = 'Y'">
					<xsl:call-template name="Format_Red_Bit_Row"/>
				</xsl:when>
				<xsl:otherwise>
				   <xsl:call-template name="Format_Green_Bit_Row"/>
				</xsl:otherwise>
			</xsl:choose>			
         </xsl:when>
         <xsl:otherwise>
           <xsl:call-template name="Format_Black_Bit_Row"/>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:for-each>
</xsl:template>

<xsl:template name="Format_Red_Row">
  <tr style="color:#FF0000;">
    <xsl:call-template name="Display_Reg_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Red_Bit_Row">
  <tr style="color:#FF0000; background-color:#FFFFFF">
    <xsl:call-template name="Display_Bit_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Black_Row">
  <tr style="color:#000000">
    <xsl:call-template name="Display_Reg_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Black_Bit_Row">
  <tr style="color:#000000">
    <xsl:call-template name="Display_Bit_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Green_Row">
  <tr style=" color:#009933; background-color:#FFFFFF">
    <xsl:call-template name="Display_Reg_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Green_Bit_Row">
  <tr style=" color:#009933; background-color:#FFFFFF">
    <xsl:call-template name="Display_Bit_Cells"/>
  </tr>
</xsl:template>

	
<xsl:template name="Display_Reg_Cells">  
	<td><xsl:value-of select="@name"/></td>		
	<xsl:choose>
		<xsl:when test="long_desc != ''"> <!-- detail is a tag, not an attribute -->
			<td wrap="wrap"><xsl:value-of select="long_desc"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td><xsl:text>&#160;&#160;</xsl:text></td>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


<xsl:template name="Display_Bit_Cells">
	<td><xsl:text>&#160;&#160;</xsl:text><xsl:value-of select="concat('&#160;&#160;&#160;&#160;&#160;&#160;',@name)"/></td>
	<xsl:choose>
		<xsl:when test="long_desc != ''">
			<td wrap="wrap"><xsl:value-of select="long_desc"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td><xsl:text>&#160;&#160;</xsl:text></td>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

</xsl:stylesheet>


